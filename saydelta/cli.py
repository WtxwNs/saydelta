"""Small local command line entry point."""

import argparse
import sys
import uuid
from pathlib import Path

from . import __version__


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Turn a script and recording into an offline listening review."
    )
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    fetch = commands.add_parser(
        "fetch-model",
        help="Download small.en using standard HTTPS with progress and bounded retries",
    )
    fetch.add_argument("destination", type=Path, help="New empty local model folder")
    check = commands.add_parser("check", help="Compare an English recording with its script")
    check.add_argument("audio", type=Path)
    check.add_argument("script", type=Path, help="UTF-8 plain text")
    check.add_argument("-o", "--output", type=Path, default=Path("review.html"))
    check.add_argument(
        "--model", default="small.en", help="Model name or local CTranslate2 model folder"
    )
    check.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    check.add_argument("--offline", action="store_true", help="Never download a model")
    args = parser.parse_args(argv)
    try:
        if args.command == "fetch-model":
            from .download import fetch_model

            fetch_model(args.destination, progress=lambda message: print(message, flush=True))
            return 0
        if args.output.suffix.lower() != ".html":
            raise ValueError("Choose an output filename ending in .html.")
        if args.output.exists():
            raise ValueError(
                "Output already exists. Choose another filename to preserve previous reviews."
            )
        if not args.output.parent.is_dir():
            raise ValueError("Output folder does not exist. Create it first.")
        if args.script.stat().st_size > 400_000:
            raise ValueError("Script is too large. Split it into chapters first.")
        script = args.script.read_text(encoding="utf-8-sig")
        from .engine import review
        from .report import write_report

        data = review(
            args.audio,
            script,
            args.model,
            args.device,
            args.offline,
            progress=lambda message: print(message, file=sys.stderr, flush=True),
        )
        data["id"] = str(uuid.uuid4())
        data["filename"] = args.audio.name
        print("Building the portable report and its listening copy…", file=sys.stderr)
        write_report(data, args.audio, args.output)
        count = sum(f["status"] == "review" for f in data["findings"])
        print(
            f"Created {args.output.resolve()}\n{count} passages to review. Recognition differences need human listening."
        )
        return 0
    except (ValueError, OSError, UnicodeError) as exc:
        print(f"Saydelta: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Saydelta: interrupted. Check the output folder before retrying.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
