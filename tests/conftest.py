import pytest
from src.config import ROOT
from src.validation import read_csv_bytes
from src.inference import load_bundle

@pytest.fixture
def sample():
    return read_csv_bytes((ROOT/"data/samples/valid_customers.csv").read_bytes())

@pytest.fixture(scope="session")
def bundle():
    return load_bundle()

