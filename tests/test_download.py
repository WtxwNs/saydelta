import http.client
import io
import urllib.error

import pytest

from saydelta.download import MODEL_FILES, fetch_model


class Response(io.BytesIO):
    def __init__(self, content, declared=None):
        super().__init__(content)
        self.headers = {"Content-Length": str(len(content) if declared is None else declared)}


def test_partial_network_transfer_retries_without_publishing_partial_file(tmp_path, monkeypatch):
    calls = []

    def retrieve(request, timeout):
        calls.append(request.full_url)
        if len(calls) == 1:
            return Response(b"{", declared=20)
        return Response(b"{}" if ".json?" in request.full_url else b"test data")

    monkeypatch.setattr("saydelta.download.urllib.request.urlopen", retrieve)
    monkeypatch.setattr("saydelta.download.time.sleep", lambda seconds: None)
    destination = tmp_path / "model"
    fetch_model(destination, progress=lambda message: None)
    assert len(calls) == 5
    assert {p.name for p in destination.iterdir()} == set(MODEL_FILES)
    assert (destination / "config.json").read_text() == "{}"


def test_download_failure_is_bounded_and_preserves_existing_files(tmp_path, monkeypatch):
    calls = []

    def fail(request, timeout):
        calls.append(request.full_url)
        raise urllib.error.URLError("offline")

    monkeypatch.setattr("saydelta.download.urllib.request.urlopen", fail)
    monkeypatch.setattr("saydelta.download.time.sleep", lambda seconds: None)
    with pytest.raises(ValueError, match="after 3 attempts"):
        fetch_model(tmp_path, progress=lambda message: None)
    assert len(calls) == 3
    assert not list(tmp_path.iterdir())
    keep = tmp_path / "model.bin.download"
    keep.write_text("existing work")
    with pytest.raises(ValueError, match="not empty"):
        fetch_model(tmp_path)
    assert keep.read_text() == "existing work" and len(calls) == 3


def test_interrupted_chunked_response_is_reported_without_traceback(tmp_path, monkeypatch):
    class Interrupted(Response):
        def read(self, size=-1):
            raise http.client.IncompleteRead(b"partial data", 100)

    calls = []

    def retrieve(request, timeout):
        calls.append(request.full_url)
        return Interrupted(b"")

    monkeypatch.setattr("saydelta.download.urllib.request.urlopen", retrieve)
    monkeypatch.setattr("saydelta.download.time.sleep", lambda seconds: None)
    with pytest.raises(ValueError, match="after 3 attempts"):
        fetch_model(tmp_path, progress=lambda message: None)
    assert len(calls) == 3
    assert not list(tmp_path.iterdir())
