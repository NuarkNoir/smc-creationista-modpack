"""
This module uploads latest artifact to modrinth platform
"""

import os
import sys
from operator import itemgetter
import requests
import pytoml as toml
from dotenv import load_dotenv

load_dotenv()

LABRINTH_API = "https://api.modrinth.com/v2"
LABRINTH_ENDPOINT = f"{LABRINTH_API}/version"
LABRINTH_TOKEN = os.getenv("LABRINTH_TOKEN")
PROJECT_ID = os.getenv("PROJECT_ID")
USERAGENT = os.getenv("USERAGENT")

if LABRINTH_TOKEN is None:
    print("Labrinth token not found")
    sys.exit(1)

if PROJECT_ID is None:
    print("Project ID not found")
    sys.exit(1)

if USERAGENT is None:
    print("User-Agent not found")
    sys.exit(1)


def create_payload(
    *,
    name: str,
    version_number: str,
    game_versions: list[str],
    version_type: str = "release",
    loaders: list[str],
    featured: bool = False,
    file_parts: list[str],
) -> dict:
    """
    This function creates correct Labrinth payload dictionary
    """
    return {
        "name": name,
        "version_number": version_number,
        "game_versions": game_versions,
        "version_type": version_type,
        "loaders": loaders,
        "featured": featured,
        "project_id": PROJECT_ID,
        "file_parts": file_parts,
    }


def get_pack_data():
    """
    This function reads pack data and returns it
    """
    with open("pack.toml", "r", encoding="utf-8") as f:
        data = toml.load(f)
    return data


def upload_latests_file():
    """
    This function reads pack data and uploads latest
    """
    try:
        data = get_pack_data()
    except FileNotFoundError:
        print("pack.toml not found")
        sys.exit(1)

    name, version = itemgetter("name", "version")(data)

    latest_pack_filename = f"{name}-{version}.mrpack"
    if not os.path.exists(latest_pack_filename):
        print(f"File not exists: {latest_pack_filename}")
        sys.exit(1)

    resp = requests.post(
        LABRINTH_ENDPOINT,
        headers={
            "Accept": "application/json",
            "Authorization": LABRINTH_TOKEN,
            "User-Agent": USERAGENT,
            "Content-Type": "multipart/form-data",
        },
        data=create_payload(
            name=version,
            version_number=version,
            game_versions=[data["versions"]["minecraft"]],
            loaders=["forge"],
            file_parts=["file"],
        ),
        files=dict(file=latest_pack_filename),
    )

    print(resp.text)


if __name__ == "__main__":
    upload_latests_file()
