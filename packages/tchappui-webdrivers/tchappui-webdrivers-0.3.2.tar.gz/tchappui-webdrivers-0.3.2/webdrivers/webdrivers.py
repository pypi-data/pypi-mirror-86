"""Main module."""

import io
import sys
import zipfile
import tarfile

import requests

chromedrivers = {
    "win32": "win32.zip",
    "linux": "linux64.zip",
    "darwin": "mac64.zip",
}

geckodrivers = {
    "win32": "win32.zip",
    "linux": "linux64.tar.gz",
    "darwin": "macos.tar.gz",
}


def install_latest_chromedriver(path="."):
    """Downloads and installs the latest chromedriver for linux64."""
    version = requests.get(
        "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    ).text
    url = (
        "https://chromedriver.storage.googleapis.com"
        f"/{version}/chromedriver_{chromedrivers[sys.platform]}"
    )
    buffer = io.BytesIO(requests.get(url).content)
    return zipfile.ZipFile(buffer).extractall(path)


def install_latest_geckodriver(path="."):
    """Downloads and installs the latest geckodriver for linux64."""
    response = requests.get(
        "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
    )
    urls = [
        asset['browser_download_url']
        for asset in response.json().get('assets', [])
        if geckodrivers[sys.platform] in asset.get('name', '')
    ]
    for url in urls:
        content = io.BytesIO(requests.get(url).content)
        if url.endswith('tar.gz'):
            return tarfile.open(fileobj=content, mode="r:gz").extractall(path)
        elif url.endswith('zip'):
            return zipfile.ZipFile(content).extractall(path)
