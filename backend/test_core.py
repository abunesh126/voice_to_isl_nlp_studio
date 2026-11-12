from pathlib import Path

from app.services.gloss import generate_gloss
from app.services.nlp import analyze_text
from app.services.evaluation import evaluate
from app.services.speech import configure_ffmpeg

def test_gloss_example():
    assert generate_gloss("I am eating an apple")["gloss"] == "I APPLE EAT"

def test_nlp():
    result = analyze_text("I am eating apples")
    assert "tokens" in result and "lemmas" in result

def test_wer():
    result = evaluate("a b c", "a c")
    assert result["wer_percent"] == 33.33

def test_ffmpeg_configuration():
    executable = Path(configure_ffmpeg())
    assert executable.is_file()

if __name__ == "__main__":
    test_gloss_example(); test_nlp(); test_wer(); test_ffmpeg_configuration()
    print("Core tests passed.")
