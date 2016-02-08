"""
tests.test_extractor
====================

Tests for extractor.

"""
import pytest
from flask import Flask

from flask_swag.extractor import Extractor


@pytest.fixture
def extractor_app():
    app = Flask(__name__)

    return app


def test_extractor(extractor_app: Flask):
    """Basic test for extractor"""
    extractor = Extractor()

    paths = extractor.extract_paths(extractor_app,
                                    exclude_endpoint=['static'])

    assert {
    } == paths
