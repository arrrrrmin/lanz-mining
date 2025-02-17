from pathlib import Path

import pytest
from scrapy import Request
from scrapy.http import TextResponse


@pytest.fixture
def file() -> Path:
    return Path("tests/data/guests.csv")


@pytest.fixture
def lanz_example() -> TextResponse:
    file_content = open("tests/html/markuslanz-example.html", "rb").read()
    url = "https://www.zdf.de/mocked-lanz-example.html"
    response = TextResponse(url=url, request=Request(url=url), body=file_content)
    return response


@pytest.fixture
def illner_example() -> TextResponse:
    file_content = open("tests/html/maybritillner-example.html", "rb").read()
    url = "https://www.zdf.de/mocked-illner-example.html"
    response = TextResponse(url=url, request=Request(url=url), body=file_content)
    return response


@pytest.fixture
def miosga_example() -> TextResponse:
    file_content = open("tests/html/carenmiosga-example.html", "rb").read()
    url = "https://www.zdf.de/mocked-miosga-example.html"
    response = TextResponse(url=url, request=Request(url=url), body=file_content)
    return response


@pytest.fixture
def maisch_example() -> TextResponse:
    file_content = open("tests/html/maischberger-example.html", "rb").read()
    url = "https://www.zdf.de/mocked-maisch-example.html"
    response = TextResponse(url=url, request=Request(url=url), body=file_content)
    return response


@pytest.fixture
def hartaberfair_example() -> TextResponse:
    file_content = open("tests/html/hartaberfair-example.html", "rb").read()
    url = "https://www1.wdr.de/daserste/mocked-hartaberfair-example.html"
    response = TextResponse(url=url, request=Request(url=url), body=file_content)
    return response
