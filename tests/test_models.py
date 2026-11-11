"""Tests for quiz_common.models module."""

from typing import Any

import pytest
from pydantic import ValidationError

from quiz_common.models import Option, Question, Quiz


def test_option_answer_type_conversion() -> None:
    """Test that non-string answer types are converted to strings."""
    # Non-string data (numbers and boolean without quotes)
    non_string_data: dict[str, Any] = {
        "name": "Test Quiz",
        "questions": [
            {
                "text": "What is 10 + 12?",
                "options": [
                    {"answer": 22, "correct": True},
                    {"answer": 3.14, "correct": False},
                    {"answer": True, "correct": False},
                ],
            },
        ],
    }

    # String data (everything with quotes)
    string_data: dict[str, Any] = {
        "name": "Test Quiz",
        "questions": [
            {
                "text": "What is 10 + 12?",
                "options": [
                    {"answer": "22", "correct": True},
                    {"answer": "3.14", "correct": False},
                    {"answer": "True", "correct": False},
                ],
            },
        ],
    }

    # Create Quiz from both versions
    quiz_from_non_string = Quiz(**non_string_data)
    quiz_from_string = Quiz(**string_data)

    # Check that both quizzes are equal
    assert quiz_from_non_string == quiz_from_string

    # Extra check: verify answer type is string
    answer = quiz_from_non_string.questions[0].options[0].answer
    assert isinstance(answer, str)
    assert answer == "22"


def test_extra_fields_quiz_forbidden() -> None:
    """Test that extra fields are forbidden in Quiz."""
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        Quiz(name="Test Quiz", questions=[], extra_field="not allowed")  # type: ignore[unknown-argument]


def test_extra_fields_question_forbidden() -> None:
    """Test that extra fields are forbidden in Question."""
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        Question(text="Test", options=[], extra_field="not allowed")  # type: ignore[unknown-argument]


def test_extra_fields_option_forbidden() -> None:
    """Test that extra fields are forbidden in Option."""
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        Option(answer="Test", correct=True, extra_field="not allowed")  # type: ignore[unknown-argument]
