"""Core functions for a simple Six Thinking Hats transcript analyzer."""

from __future__ import annotations

import os
import re
from pathlib import Path

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

from prompts import (
    FORMATTER_EXAMPLE_INPUT,
    FORMATTER_EXAMPLE_OUTPUT,
    FORMATTER_SYSTEM_PROMPT,
    HAT_ASSIGNMENT_EXAMPLE_INPUT,
    HAT_ASSIGNMENT_EXAMPLE_OUTPUT,
    HAT_ASSIGNMENT_SYSTEM_PROMPT,
    MEANING_EXTRACTOR_EXAMPLE_INPUT,
    MEANING_EXTRACTOR_EXAMPLE_OUTPUT,
    MEANING_EXTRACTOR_SYSTEM_PROMPT,
)

HATS = ("red", "black", "white", "blue", "green", "yellow")
DOMINANT_WEIGHT = 1.0
SECONDARY_WEIGHT = 0.3

HAT_COLORS = {
    "red": "red",
    "black": "black",
    "white": "white",
    "blue": "blue",
    "green": "green",
    "yellow": "yellow",
}

HAT_LABELS = {
    "red": "Red Hat",
    "black": "Black Hat",
    "white": "White Hat",
    "blue": "Blue Hat",
    "green": "Green Hat",
    "yellow": "Yellow Hat",
}


def make_openai_client():
    """Create an OpenAI client using OPENAI_API_KEY from the environment."""

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise ImportError("Install the OpenAI SDK first: pip install openai") from exc

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY before running the analyzer.")

    return OpenAI()


def ask_model(client, messages: list[dict[str, str]], model: str) -> str:
    """Send one prompt to the model and return the text response."""

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )

    text = response.choices[0].message.content
    if not text:
        raise RuntimeError("The model returned an empty response.")

    return text.strip()


def format_transcript(transcript: str, client, model: str) -> str:
    """Clean punctuation and structure a raw transcript into dialogue format."""

    messages = [
        {"role": "system", "content": FORMATTER_SYSTEM_PROMPT},
        {"role": "user", "content": FORMATTER_EXAMPLE_INPUT},
        {"role": "assistant", "content": FORMATTER_EXAMPLE_OUTPUT},
        {"role": "user", "content": transcript.strip()},
    ]
    return ask_model(client, messages, model)


def extract_meaningful_information(formatted_transcript: str, client, model: str) -> str:
    """Remove filler while keeping the meaningful content of the transcript."""

    messages = [
        {"role": "system", "content": MEANING_EXTRACTOR_SYSTEM_PROMPT},
        {"role": "user", "content": MEANING_EXTRACTOR_EXAMPLE_INPUT},
        {"role": "assistant", "content": MEANING_EXTRACTOR_EXAMPLE_OUTPUT},
        {"role": "user", "content": formatted_transcript.strip()},
    ]
    return ask_model(client, messages, model)


def assign_thinking_hats(meaningful_transcript: str, client, model: str) -> str:
    """Label each sentence with a dominant and secondary thinking hat."""

    messages = [
        {"role": "system", "content": HAT_ASSIGNMENT_SYSTEM_PROMPT},
        {"role": "user", "content": HAT_ASSIGNMENT_EXAMPLE_INPUT},
        {"role": "assistant", "content": HAT_ASSIGNMENT_EXAMPLE_OUTPUT},
        {"role": "user", "content": meaningful_transcript.strip()},
    ]
    return ask_model(client, messages, model)


def count_hats(annotated_text: str, secondary_weight: float = SECONDARY_WEIGHT) -> dict[str, float]:
    """Count dominant and secondary hat labels in the model output."""

    counts = {}

    for hat in HATS:
        dominant = len(re.findall(rf"\({hat}\)", annotated_text, flags=re.IGNORECASE))
        secondary = len(re.findall(rf"\({hat}_s\)", annotated_text, flags=re.IGNORECASE))
        score = dominant * DOMINANT_WEIGHT + secondary * secondary_weight

        if score > 0:
            counts[hat] = round(score, 2)

    return counts


def plot_hat_distribution(hat_counts: dict[str, float], output_path: str | Path) -> None:
    """Save a README-ready pie chart showing weighted thinking-hat distribution."""

    if not hat_counts:
        raise ValueError("No hat labels found, so no chart can be created.")

    ordered_counts = dict(
        sorted(hat_counts.items(), key=lambda item: item[1], reverse=True)
    )
    labels = [HAT_LABELS[hat] for hat in ordered_counts]
    sizes = list(ordered_counts.values())
    colors = [HAT_COLORS[hat] for hat in ordered_counts]
    legend_labels = [
        f"{label} — {score:g}" for label, score in zip(labels, sizes)
    ]

    fig, ax = plt.subplots(figsize=(9, 6), facecolor="white")
    _, _, autotexts = ax.pie(
        sizes,
        labels=None,
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        counterclock=False,
        pctdistance=0.72,
        wedgeprops={"edgecolor": "white", "linewidth": 2.0},
    )

    for index, autotext in enumerate(autotexts):
        red, green, blue = mcolors.to_rgb(colors[index])
        brightness = 0.299 * red + 0.587 * green + 0.114 * blue
        autotext.set_color("black" if brightness > 0.5 else "white")
        autotext.set_fontsize(11)
        autotext.set_fontweight("bold")

    ax.set_title("Thinking Hat Distribution", fontsize=18, fontweight="bold", pad=18)
    ax.legend(
        legend_labels,
        title="Weighted counts",
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        frameon=False,
    )
    ax.axis("equal")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, bbox_inches="tight", dpi=180)
    plt.close(fig)


def analyze_transcript(transcript: str, model: str = "gpt-4o-mini") -> dict[str, object]:
    """Run the full analysis pipeline and return all outputs."""

    if not transcript.strip():
        raise ValueError("Transcript cannot be empty.")

    client = make_openai_client()
    formatted = format_transcript(transcript, client, model)
    meaningful = extract_meaningful_information(formatted, client, model)
    annotated = assign_thinking_hats(meaningful, client, model)
    counts = count_hats(annotated)

    return {
        "formatted_transcript": formatted,
        "meaningful_transcript": meaningful,
        "annotated_transcript": annotated,
        "hat_counts": counts,
    }
