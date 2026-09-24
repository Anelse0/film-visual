"""Read-only English word-budget check; not a Midjourney tokenizer or parser."""
import argparse
import json
from pathlib import Path
import re


BUDGETS = {"simple": (20, 50), "standard": (50, 90), "complex": (90, 140)}
WORD = re.compile(r"[A-Za-z0-9]+(?:['’\-][A-Za-z0-9]+)*")
URL = re.compile(r'https?://[^\s"<>]+')
PARAMETER = re.compile(r"--[A-Za-z][A-Za-z0-9-]*(?=\s|$)")


def split_body(prompt):
    if "```" in prompt:
        raise ValueError("Pass one plain prompt, without Markdown fences or commentary.")
    quoted = False
    escaped = False
    for index, char in enumerate(prompt):
        if escaped:
            escaped = False
            continue
        if quoted and char == "\\":
            escaped = True
            continue
        if char == '"':
            quoted = not quoted
        if not quoted and (index == 0 or prompt[index - 1].isspace()):
            if PARAMETER.match(prompt, index):
                return prompt[:index], prompt[index:]
    if quoted:
        raise ValueError("Unclosed double quote in descriptive text.")
    return prompt, ""


def measure(prompt, budget="standard", max_words=None):
    if budget not in BUDGETS:
        raise ValueError("Unknown budget.")
    if max_words is not None and (type(max_words) is not int or max_words < 1):
        raise ValueError("The explicit user word limit must be a positive integer.")
    body, parameters = split_body(prompt.strip())
    description = URL.sub("", body).strip()
    if not description:
        raise ValueError("No descriptive text to measure.")
    applicable = not any(c.isalpha() and not c.isascii() for c in description)
    if not applicable and max_words is not None:
        raise ValueError("English word limits cannot validate non-English or mixed-language text.")
    words = len(WORD.findall(description)) if applicable else None
    return {
        "measurement": "English lexical words, not Midjourney tokens",
        "budget": budget,
        "soft_range": list(BUDGETS[budget]),
        "word_budget_applicable": applicable,
        "body_words": words,
        "body_characters_excluding_urls": len(description),
        "over_soft_budget": words > BUDGETS[budget][1] if applicable else None,
        "user_max_words": max_words,
        "within_user_limit": words <= max_words if max_words is not None else None,
        "parameter_tail_present": bool(parameters),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path, help="Existing UTF-8 plain-prompt file; never modified.")
    source.add_argument("--text", help="One plain prompt; no file is created.")
    parser.add_argument("--budget", choices=BUDGETS, default="standard")
    parser.add_argument("--max-words", type=int, help="Only for a user-specified hard word limit.")
    args = parser.parse_args()
    try:
        prompt = args.input.read_text(encoding="utf-8-sig") if args.input else args.text
        result = measure(prompt, args.budget, args.max_words)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False))
    return 1 if result["within_user_limit"] is False else 0


if __name__ == "__main__":
    raise SystemExit(main())
