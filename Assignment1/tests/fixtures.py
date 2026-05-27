
import pytest

from ..src.app import create_app
from ..src.model.agency import Agency
from .testdata import populate


@pytest.fixture()
def app():
    yield create_app()


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture()
def agency(app):
    agency = Agency.get_instance()
    agency.reset()
    populate(agency)
    yield agency

