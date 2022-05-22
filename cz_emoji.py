from collections import OrderedDict
from typing import Any, Dict, List

import emoji
from commitizen.cz.base import BaseCommitizen
from commitizen.cz.utils import multiple_line_breaker, required_validator
from commitizen.defaults import MAJOR, MINOR, PATCH, Questions

__all__ = ["CommitizenEmojiCz"]

def parse_scope(text):
    if not text:
        return ""

    scope = text.strip().split()
    if len(scope) == 1:
        return scope[0]

    return emoji.emojize(" ".join(scope))


def parse_subject(text):
    if isinstance(text, str):
        text = text.strip(".").strip()

    return required_validator(text, msg="Subject is required.")


class ConventionalEmojiCz(BaseCommitizen):
    bump_pattern = r"^(BREAKING CHANGE|🎉? ?feat|🔨? ?fix|➗? ?refactor|🧼? ?correction)(\(.+\))?(!)?"
    bump_map = OrderedDict(
        (
            (r"^.+!$", MAJOR),
            (r"^BREAKING CHANGE", MAJOR),
            (r"^🎉? ?feat", MINOR),
            (r"^🔨? ?fix", PATCH),
        )
    )
    change_type_map = {
        "feat": "Feat",
        "fix": "Fix",
        "refactor": "Refactor",
        "correction": "Correction",
    }
    
    def questions(self) -> Questions:
        questions: Questions = [
            {
                "name": "prefix",
                "type": "list",
                "message": "Select the type of change you are committing",
                "choices": [
                    {
                        "value": "🎉 feat",
                        "name": "🎉 feat: (Bumps MINOR) Add a feature (captures new items; in particular, anything the end user can see)",
                    },
                    {
                        "value": "🔨 fix",
                        "name": "🔨 fix: (Bumps PATCH) Fix an item (captures modifications; item must exist and the change affect its behavior).",
                    },
                    {
                        "value": "➗ refactor",
                        "name": "➗ refactor: (Bumps nothing) A change that does not add features or modify behavior.",
                    },
                    {
                        "value": "🧼 correction",
                        "name": "🧼 correction: (Bumps nothing) A fix that does not add features or modify behavior (e.g. typos, formatting, white-space, etc.)",
                    },
                ],
            },
            {
                "name": "scope",
                "type": "input",
                "message": (
                    "Scope. Enter the scope of the change (e.g. docs/test/ci/perf, a file name, or a category).\n"
                    "Enter MarkDown emojis with ':emoji:' style syntax (e.g. :tada:):\n"
                ),
                "filter": parse_scope,
            },
            {
                "name": "subject",
                "type": "input",
                "message": (
                    "Subject. Concise description of the changes. Imperative, lower case and no final dot:\n"
                ),
                "filter": parse_subject,
            },
            {
                "name": "body",
                "type": "input",
                "message": (
                    "Body. Motivation for the change and contrast this "
                    "with previous behavior:\n"
                ),
                "filter": multiple_line_breaker,
            },
            {
                "name": "is_breaking_change",
                "type": "confirm",
                "message": "Is this a BREAKING CHANGE? (Bumps MAJOR)",
                "default": False,
            },
            {
                "type": "input",
                "name": "footer",
                "message": (
                    "Footer. Information about Breaking Changes and "
                    "reference issues that this commit closes: (press [enter] to skip)\n"
                ),
            },
        ]
        return questions

    def message(self, answers: dict) -> str:
        prefix = answers["prefix"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        is_breaking_change = answers["is_breaking_change"]
        footer = answers["footer"]

        if scope:
            scope = f"({scope})"
        if body:
            body = f"\n\n{body}"
        if is_breaking_change:
            body = f"BREAKING CHANGE 🚨: {footer}"
        if footer:
            footer = f"\n\n{footer}"

        message = f"{prefix}{scope}: {subject}{body}{footer}"

        return message


discover_this = ConventionalEmojiCz
