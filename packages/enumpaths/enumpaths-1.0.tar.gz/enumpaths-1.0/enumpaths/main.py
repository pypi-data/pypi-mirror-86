#!/usr/bin/python3
import click
import fileinput
import requests

settings = {
    "headers": {
        "User-Agent": "Mozilla/5.0 (X11; GNU/Linux) AppleWebKit/601.1 (KHTML,like Gecko) Tesla QtCarBrowser Safari/601.1"
    },
        "proxies": {
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080"
        },
}


@click.command()
@click.argument("host")
@click.argument("file")
def cli(host, file):
    """
    1. Takes paths from a file e.g. gobuster output.\n
    2. Sends a proxied GET request to each URL (for Burp).\n

    If something is not working
    e.g. you're not using port 8080 check settings in this package/main.py.\n

    Default is localhost:8080, Tesla carbrowser UA header.\n

    HOST: e.g. https://example.com\n
    FILE: Has /paths e.g. gobuster -n output.\n
    USAGE: $ enumpaths https://example.com urls.txt\n
           $ cat urls.txt | enumpaths https://example.com -\n
    """
    for path in fileinput.input(file):
        url = str(host) + str(path.strip())
        
        response = requests.get(url=url, headers=settings["headers"], proxies=settings["proxies"])

        click.echo(f"{response.status_code} -> {url}")
