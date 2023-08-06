import boto3
import botocore
import os
from configparser import ConfigParser
from datetime import datetime

from mentaws.config import get_platform_config

platform_config = get_platform_config()
config_file_path = os.path.join(
    platform_config["aws_directory"], platform_config["config_file_name"]
)


def get_token(
    key_id: str,
    secret_access_key: str,
    duration_seconds: int = platform_config["default_duration_seconds"],
    region: str = "ap-southeast-1",
) -> dict:
    """
    :param key_id: AWS key id
    :param secret_access_key: AWS secret access key
    :param region: AWS region
    :param duration_seconds: Duration of access keys
    :return: Dict containing temporary key_id, secret_access_key, and session_token
    """

    client = boto3.client(
        "sts",
        region_name=region,
        endpoint_url=f"https://sts.{region}.amazonaws.com",
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_access_key,
    )
    try:
        response = client.get_session_token(DurationSeconds=duration_seconds)

        token = {
            "aws_access_key_id": response["Credentials"]["AccessKeyId"],
            "aws_secret_access_key": response["Credentials"]["SecretAccessKey"],
            "aws_session_token": response["Credentials"]["SessionToken"],
            "aws_token_expiry_time_human": format_time(
                response["Credentials"]["Expiration"]
            ),
            "aws_token_expiry_time_machine": (
                response["Credentials"]["Expiration"]
            ).isoformat(),
        }
    except botocore.exceptions.ClientError:
        token = {
            "aws_access_key_id": "ERROR",
            "aws_secret_access_key": "ERROR",
            "aws_token_expiry_time_human": "  ***FAILED***  ",
            "aws_token_expiry_time_machine": "  ***FAILED***  ",
        }

    return token


def get_aws_config() -> ConfigParser:
    """
    :param platform_config: platform configuration
    :return:
    """

    aws_config = ConfigParser()
    aws_config.read(config_file_path)

    return aws_config


def get_region(profile: str) -> str:
    """
    Get region for profile in this priority:
        * Region of profile in aws config file
        * Region of 'default' profile in config file
        * default_region setting in config
    """

    aws_config = get_aws_config()

    try:
        region = aws_config[f"profile {profile}"]["region"]
    except KeyError:
        region = aws_config["default"]["region"]

    return region


def format_time(expiration_time: datetime):

    local_expiration_time = expiration_time.astimezone()

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day = days[local_expiration_time.weekday()]
    time = f"{local_expiration_time.hour:02d}:{local_expiration_time.minute:02d}"
    tzname = local_expiration_time.tzname()

    return f"{day} {time} tz:{tzname}"
