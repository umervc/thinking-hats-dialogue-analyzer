"""Command-line runner for the Six Thinking Hats transcript analyzer."""

from __future__ import annotations

import argparse
from pathlib import Path

from thinking_hats import analyze_transcript, plot_hat_distribution


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze a transcript with the Six Thinking Hats framework."
    )
    parser.add_argument("transcript_file", type=Path, help="Path to a .txt transcript file.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("analysis.txt"),
        help="Where to save the text analysis. Default: analysis.txt",
    )
    parser.add_argument(
        "--chart",
        type=Path,
        default=Path("hat_distribution.png"),
        help="Where to save the pie chart. Default: hat_distribution.png",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model to use. Default: gpt-4o-mini",
    )
    return parser


def build_report(result: dict[str, object]) -> str:
    counts = result["hat_counts"]
    counts_text = "\n".join(f"{hat}: {score}" for hat, score in counts.items())

    return "\n\n".join(
        [
            "# Formatted transcript",
            str(result["formatted_transcript"]),
            "# Meaningful transcript",
            str(result["meaningful_transcript"]),
            "# Thinking hats annotation",
            str(result["annotated_transcript"]),
            "# Weighted hat counts",
            counts_text,
        ]
    )


def main() -> None:
    args = build_parser().parse_args()

    transcript = args.transcript_file.read_text(encoding="utf-8")
    result = analyze_transcript(transcript, model=args.model)

    report = build_report(result)
    args.output.write_text(report, encoding="utf-8")
    plot_hat_distribution(result["hat_counts"], args.chart)

    print(f"Saved text analysis to: {args.output}")
    print(f"Saved chart to: {args.chart}")


if __name__ == "__main__":
    main()
