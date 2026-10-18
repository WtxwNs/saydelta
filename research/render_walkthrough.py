"""Edited 40-second walkthrough from actual browser captures, not a UI mockup.

Silent still captures are held for reading; timings are NOT processing latency.
Open the accompanying HTML for actual interactive audio playback.
"""
from pathlib import Path
import json

import av
from PIL import Image, ImageDraw, ImageFont

report_html = Path('examples/garden-review-v2.html').read_text(encoding='utf-8')
report_data = json.loads(report_html.split('<script id="report-data" type="application/json">')[1].split('</script>')[0])
seconds = report_data['provenance']['processing_seconds']
captions = [
    ("01", 6, "INPUT: garden.txt + a 46.8-second synthetic recording.",
     "Three deliberate edits: a missing sentence, one changed number, one repeated sentence."),
    ("02", 7, "OUTPUT: a portable HTML review, produced by the actual CLI.",
     f"CPU recognition + rechecks: {seconds:.2f} seconds on this machine; model loading excluded."),
    ("03", 6, "Click a suspect passage to hear its nearby context.",
     "Silent walkthrough: open garden-review-v2.html to listen to the embedded recording."),
    ("04", 7, "The script says ONE. The recognizer heard TWO.",
     "Recognition can be wrong. Listen before deciding; a finding is not a verified error."),
    ("05", 7, "Keep a pickup decision and a precise note.",
     "Export decisions as JSON and pass the same offline report to a collaborator."),
    ("06", 7, "A repeated passage auditions both copies.",
     "Local, English-only word review. Names and human audiobooks remain difficult."),
]
font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 25)
small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 19)
with av.open("docs/walkthrough.mp4", "w") as out:
    stream = out.add_stream("libx264", rate=10)
    stream.width, stream.height = 1280, 1024
    stream.pix_fmt = "yuv420p"
    stream.options = {"crf": "21", "preset": "medium"}
    for name, seconds, title, detail in captions:
        source = Image.open(Path("docs/demo-frames", name + ".png")).convert("RGB")
        source.thumbnail((1280, 900))
        canvas = Image.new("RGB", (1280, 1024), "#f7f6f2")
        if name == '01':
            draw = ImageDraw.Draw(canvas)
            heading = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 48)
            draw.text((45, 85), "A script + a recording", font=heading, fill="#133f37")
            draw.text((45, 150), "become a listening inbox.", font=heading, fill="#133f37")
            draw.text((45, 270), "Actual input: examples/garden.txt", font=font, fill="#333333")
            source = source.resize((1190, round(source.height * 1190/source.width)))
            canvas.paste(source, (45, 325))
            draw.text((45, 720), "Recording: examples/garden.wav · 46.8 seconds", font=font, fill="#133f37")
            draw.text((45, 765), "Local CLI → one self-contained review.html", font=font, fill="#133f37")
        else:
            canvas.paste(source, ((1280-source.width)//2, 0))
        draw = ImageDraw.Draw(canvas)
        draw.rectangle((0, 900, 1280, 1024), fill="#133f37")
        draw.text((24, 912), title, font=font, fill="white")
        draw.text((24, 950), detail, font=small, fill="#e1eee8")
        draw.text((24, 986), "Actual browser captures · edited holds · silent · planted demo faults · not real-time", font=small, fill="#b8d9cc")
        for _ in range(seconds * 10):
            for packet in stream.encode(av.VideoFrame.from_image(canvas)):
                out.mux(packet)
    for packet in stream.encode():
        out.mux(packet)
print("docs/walkthrough.mp4: 40 seconds, edited real UI captures, no audio")
