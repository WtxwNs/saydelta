import json
from types import SimpleNamespace

import numpy as np
import pytest

from saydelta.alignment import align
from saydelta.audio import decode
from saydelta.cli import main
from saydelta.engine import recheck
from saydelta.report import write_report


def words(text):
    return [{"word": w, "start": i, "end": i + 0.8} for i, w in enumerate(text.split())]


def test_edge_omissions_have_listenable_bounded_context():
    for script, heard in [
        ("first middle last", "middle last"),
        ("first middle last", "first middle"),
    ]:
        findings = align(script, words(heard), 3)
        assert len(findings) == 1
        f = findings[0]
        assert f["kind"] == "omission"
        assert script[f["script_start"] : f["script_end"]] == f["expected"]
        assert 0 <= f["start"] < f["end"] <= 3


def test_numeric_change_survives_spelling_normalization():
    assert not align("We have 6 neighbours.", words("We have six neighbors"), 5)
    assert align("We have 6 neighbours.", words("We have nine neighbors"), 5)[0]["expected"] == "6"


def test_repetition_context_contains_both_copies():
    findings = align("we carry the box home", words("we carry the box carry the box home"), 8)
    assert len(findings) == 1
    assert findings[0]["kind"] == "repetition"
    assert findings[0]["start"] <= 1 and findings[0]["end"] >= 6.8


def test_multiple_faults_keep_unchanged_sentence_anchors():
    script = "We begin the tour. The flowers stay near the gate. Each family gets one small bed to water. Before planting we test the soil. We finish the day together."
    heard = "We begin the tour. Each family gets two small bed to water. Before planting we test the soil. Before planting we test the soil. We finish the day together."
    findings = align(script, words(heard), 50)
    assert len(findings) == 3
    assert {f["kind"] for f in findings} == {"omission", "replacement", "repetition"}
    assert any(f["expected"] == "one" and f["heard"] == "two" for f in findings)


def test_long_replacement_cannot_be_dismissed_as_correct_copy():
    class NoCall:
        def transcribe(self, *args, **kwargs):
            pytest.fail("A long insertion must not be downgraded by re-recognizing a correct copy")

    finding = {
        "kind": "replacement",
        "expected": "A",
        "heard": "A damaged cable or a missing cover",
        "start": 1,
        "end": 4,
        "script_start": 0,
        "script_end": 1,
    }
    result = recheck(
        NoCall(),
        np.zeros(160000),
        "A damaged cable or a missing cover needs repair today",
        [finding],
    )
    assert result[0]["status"] == "review"


def test_recheck_never_receives_reference_prompt():
    script = "We carry the blue box across the quiet room before the morning meeting starts"

    class Recognizer:
        def transcribe(self, audio, **kwargs):
            assert not any(k in kwargs for k in ["initial_prompt", "prefix", "hotwords"])
            assert kwargs["condition_on_previous_text"] is False
            return iter([SimpleNamespace(text=script)]), None

    f = align(script, words(script.replace("blue", "red")), 20)
    result = recheck(Recognizer(), np.zeros(320000), script, f)
    assert result[0]["status"] == "not_reproduced"
    assert result[0]["heard"] == "red"
    assert result[0]["recheck"]["heard"] == script


def write_wav(path, values):
    import wave

    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(16000)
        out.writeframes(values.astype("<i2").tobytes())


def test_decode_silence_corruption_and_valid_audio(tmp_path):
    path = tmp_path / "input.wav"
    write_wav(path, np.zeros(16000))
    with pytest.raises(ValueError, match="silent"):
        decode(path)
    path.write_bytes(b"This is not an audio file")
    with pytest.raises(ValueError, match="decode"):
        decode(path)
    write_wav(path, 1000 * np.sin(np.arange(16000) * 0.1))
    audio = decode(path)
    assert len(audio) == 16000 and np.isfinite(audio).all() and abs(audio).max() > 0.02


def test_report_embeds_safe_json_and_does_not_overwrite(tmp_path, monkeypatch):
    monkeypatch.setattr("saydelta.report.review_audio", lambda path: "YWJj")
    payload = {"id": "fixed", "script": "</script><img src=x onerror=alert(1)>", "findings": []}
    destination = tmp_path / "report.html"
    write_report(payload, "unused.wav", destination)
    html = destination.read_text(encoding="utf-8")
    encoded = html.split('<script id="report-data" type="application/json">')[1].split("</script>")[
        0
    ]
    assert json.loads(encoded)["script"] == payload["script"]
    assert "<img src=x" not in html
    assert "connect-src 'none'" in html
    with pytest.raises(ValueError, match="exists"):
        write_report(payload, "unused.wav", destination)
    assert destination.read_text(encoding="utf-8") == html


def test_cli_input_failure_preserves_existing_report(tmp_path, capsys):
    output = tmp_path / "review.html"
    output.write_text("previous review")
    assert main(["check", "missing.wav", "missing.txt", "-o", str(output)]) == 2
    assert "already exists" in capsys.readouterr().err
    assert output.read_text() == "previous review"
