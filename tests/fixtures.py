import pytest
import tempfile


@pytest.fixture(scope="function")
def tempfile_log(monkeypatch):
    tempdir = tempfile.mkdtemp()
    get_temp_directory = lambda: tempdir
    monkeypatch.setattr("wurst.filesystem.get_base_directory", get_fake_directory)
