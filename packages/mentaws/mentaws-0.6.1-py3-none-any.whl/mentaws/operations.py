from configparser import ConfigParser, NoOptionError
import json
import os
import sys

import sqlite3

from mentaws.config import get_platform_config
from mentaws.cryptographic_operations import setup_key, encrypt_keys, decrypt_keys

from typing import List


# General configuration
config = get_platform_config()
table_name = config["default_table_name"]
app_name = config["default_app_name"]
key_name = config["encryption_key_name"]

mentaws_db_path = os.path.join(config["aws_directory"], config["database_file"])
creds_file_path = os.path.join(config["aws_directory"], config["creds_file_name"])


def setup_new_db() -> List[str]:
    """
    Creates a new sqlite database, and populates it with the credentials from the creds file
    """

    if not os.path.isfile(mentaws_db_path):

        # Create database
        conn = sqlite3.connect(mentaws_db_path)
        db = conn.cursor()
        db.execute(f"DROP TABLE IF EXISTS {table_name}")
        db.execute(
            f"CREATE TABLE {table_name} (profile text PRIMARY KEY, \
                                    aws_access_key_id text NOT NULL, \
                                    aws_secret_access_key text NOT NULL, \
                                    other_options text \
                                    )"
        )
        conn.commit()
        conn.close()

        # setup encryption key
        setup_key(app_name, key_name)

        # Read credentials from existing file
        creds = ConfigParser()
        with open(creds_file_path, "r") as creds_file:
            creds.read_string(creds_file.read())

        # Write out to database
        profiles = write_creds_to_db(creds)
    else:
        profiles = None

    return profiles


def list_profiles_in_db() -> List[str]:
    """
    List all profiles in database
    """
    if os.path.isfile(mentaws_db_path):
        conn = sqlite3.connect(mentaws_db_path)
        conn.row_factory = sqlite3.Row
        db = conn.cursor()
        db.execute(f"SELECT profile FROM {table_name}")

        profiles = [row["profile"] for row in db]

        conn.close()

    else:
        sys.exit("No database table, DB might has not been setup or is corrupted.")

    return profiles


def get_plaintext_credentials(profiles: str = "", all: bool = False) -> List[dict]:
    """
    Args:
      profiles: comma separated string of aws_profiles to retrieve
      all: Retrieve all profiles (by default only those with credentials are returned)
    return:
      creds = List of dicts, each with keys (profile, aws_access_key_id, aws_secret_access_key)
    """

    creds = list()
    conn = sqlite3.connect(mentaws_db_path)
    conn.row_factory = sqlite3.Row
    db = conn.cursor()

    # Get all profiles in DB
    try:
        # Select all profiles (even those without creds)
        if all:
            db.execute(f"SELECT * FROM {table_name} ORDER BY profile")
        # Select only profiles with creds
        elif len(profiles) == 0:
            db.execute(
                f"SELECT * FROM {table_name} WHERE aws_access_key_id != '' ORDER BY profile"
            )
        else:
            profile_list = profiles.split(",")
            # Select only one profile
            if len(profile_list) == 1:
                db.execute(
                    f"SELECT * FROM {table_name} WHERE profile = ? AND aws_access_key_id != '' ORDER BY profile",
                    (profile_list[0],),
                )
            # Select a list of profiles
            else:
                db.execute(
                    f"SELECT * FROM {table_name} WHERE profile IN {(str(tuple(profile_list)))} AND aws_access_key_id != '' ORDER BY profile"
                )
    except sqlite3.OperationalError:
        sys.exit("No database table, DB might has not been setup or is corrupted.")

    # generate dictionary for all fields
    for row in db:
        # Sqlite3 rows are not real dictionaries, do not support easy copying
        temp_row = dict()
        for key in row.keys():
            temp_row[key] = row[key]

        # handle additional fields
        other_options = json.loads(temp_row["other_options"])
        del temp_row["other_options"]
        for key in other_options.keys():
            temp_row[key] = other_options[key]
        creds.append(temp_row)

    # append with plaintext keys, we do it this way, so that only one call is made to get the decryption key
    # This reduces the number of times the user has to enter the keychain password
    plaintext_keys = decrypt_keys(profiles=creds, app_name=app_name, key_name=key_name)
    for cred in creds:
        cred["aws_secret_access_key"] = plaintext_keys[cred["profile"]]

    # return all data back (with plaintext AKIA keys)
    return creds


def write_creds_file(config: ConfigParser, replace: bool = True):

    """
    Writes out data in config to credentials file
    Args:
      config: ConfigParser to write out too

      **Future addition**
      replace: if True, replaces entire credentials file. If False, only over-writes existing sections
    """

    creds = ConfigParser()

    if not replace:
        creds.read(filenames=[creds_file_path], encoding="utf-8")

    creds.read_dict(configparser_to_dict(config))
    with open(creds_file_path, "w") as creds_file:
        creds.write(creds_file)

    return


def check_new_profiles() -> dict:

    creds = ConfigParser()
    creds.read(filenames=[creds_file_path], encoding="utf-8")
    existing_profiles = list_profiles_in_db()

    new_profiles = dict()
    for section in creds.sections():
        try:
            key_id = creds.get(section, "aws_access_key_id")
            if key_id[:4] == "AKIA" and section not in existing_profiles:
                new_section = {}
                for option in creds.options(section):
                    new_section[option] = creds.get(section, option)
                new_profiles[section] = new_section
        except NoOptionError:
            pass

    # Write new profiles to database
    if len(new_profiles.keys()) > 0:
        new_creds = ConfigParser()
        new_creds.read_dict(new_profiles)
        write_creds_to_db(new_creds)

    return new_profiles


def write_creds_to_db(creds: ConfigParser) -> List[str]:

    conn = sqlite3.connect(mentaws_db_path)
    db = conn.cursor()

    rows_to_write = list()

    for k, section in enumerate(creds.sections()):
        temp_profile = dict()
        temp_profile["profile"] = section

        try:
            temp_profile["aws_access_key_id"] = creds.get(section, "aws_access_key_id")
            temp_profile["aws_secret_access_key"] = creds.get(
                section, "aws_secret_access_key"
            )

        except NoOptionError:  # doesn't have credentials
            temp_profile["aws_access_key_id"] = ""
            temp_profile["aws_secret_access_key"] = ""

        other_options = dict()
        for option in creds[section]:
            if option not in ["aws_access_key_id", "aws_secret_access_key"]:
                other_options[option] = creds.get(section, option)

        temp_profile["other_options"] = json.dumps(other_options)
        rows_to_write.append(temp_profile)

    # append with encrypted keys, we do it this way, so that one call can be made to cryptographic operations, and retrieve the secret key once!
    # This reduces the number of times the user has to enter the keychain password
    encrypted_keys = encrypt_keys(
        profiles=rows_to_write, app_name=app_name, key_name=key_name
    )

    for row in rows_to_write:
        profile = row["profile"]
        db.execute(
            f"INSERT INTO {table_name} (profile, aws_access_key_id, aws_secret_access_key, other_options) VALUES(?,?,?,?)",
            (
                profile,
                row["aws_access_key_id"],
                encrypted_keys[profile],
                row["other_options"],
            ),
        )

    conn.commit()
    conn.close()
    profiles = [profile for profile in creds.sections()]

    return profiles


def remove_profile_from_db(profile_name: str) -> bool:

    conn = sqlite3.connect(mentaws_db_path)
    conn.row_factory = sqlite3.Row
    db = conn.cursor()

    try:
        db.execute(f"DELETE FROM {table_name} WHERE profile = ?", (profile_name,))
        conn.commit()
        response = True
    except (IndexError, KeyError):
        response = False
    except sqlite3.OperationalError:
        sys.exit("No database table, DB might has not been setup or is corrupted.")

    conn.close()
    return response


def check_profile_in_db(profile_name: str) -> bool:

    conn = sqlite3.connect(mentaws_db_path)
    conn.row_factory = sqlite3.Row
    db = conn.cursor()
    db.execute(f"SELECT profile FROM {table_name} WHERE profile=?", (profile_name,))

    row = [item for item in db]
    if len(row) > 0:
        response = True
    else:
        response = False

    return response


def configparser_to_dict(config: ConfigParser) -> dict:

    return {section: dict(config[section]) for section in config.sections()}


def creds_file_contents() -> ConfigParser:

    creds = ConfigParser()
    creds.read(filenames=[creds_file_path], encoding="utf-8")

    return creds


def remove_mentaws_db() -> str:

    try:
        os.remove(mentaws_db_path)
    except OSError:
        pass

    return config["database_file"]
