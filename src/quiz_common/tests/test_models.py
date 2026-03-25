"""Tests for quiz_common.models module."""

import pytest

from quiz_common.models import Option, Question, Quiz


def test_option_answer_type_conversion():
    """Test that non-string answer types are converted to strings."""
    # Non-string data (numbers and boolean without quotes)
    non_string_data = {
        "name": "Test Quiz",
        "questions": [
            {
                "text": "What is 10 + 12?",
                "options": [
                    {"answer": 22, "correct": True},
                    {"answer": 3.14, "correct": False},
                    {"answer": True, "correct": False},
                ]
            }
        ]
    }

    # String data (everything with quotes)
    string_data = {
        "name": "Test Quiz",
        "questions": [
            {
                "text": "What is 10 + 12?",
                "options": [
                    {"answer": "22", "correct": True},
                    {"answer": "3.14", "correct": False},
                    {"answer": "True", "correct": False},
                ]
            }
        ]
    }

    # Create Quiz from both versions
    quiz_from_non_string = Quiz(**non_string_data)
    quiz_from_string = Quiz(**string_data)

    # Check that both quizzes are equal
    assert quiz_from_non_string == quiz_from_string

    # Extra check: verify answer type is string
    assert isinstance(quiz_from_non_string.questions[0].options[0].answer, str)
    assert quiz_from_non_string.questions[0].options[0].answer == "22"
