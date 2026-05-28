"""Shared data models used by quiz components."""

import string

from pydantic import BaseModel, Field, field_validator


class Option(BaseModel):
    """Single answer option for a question."""

    answer: str
    correct: bool

    @field_validator("answer", mode="before")
    @classmethod
    def convert_to_string(cls, v: str | bool | float) -> str:  # noqa: FBT001
        """Allow int, float, bool and convert them to string."""
        if isinstance(v, (int, float, bool)):
            return str(v)
        return v

    def ask(self) -> dict:
        """Return a dictionary representation of the option, used when sending json."""
        return {
            "answer": self.answer,
            "correct": False,
        }


class Question(BaseModel):
    """Quiz question with text, options and optional time limit."""

    text: str
    time_limit: int | None = None
    options: list[Option] = Field(default_factory=list)

    def ask(self) -> dict:
        """Return a representation of the question which is sent to the players."""
        return {
            "type": "question",
            "text": self.text,
            "options": [opt.ask() for opt in self.options],
        }

    def print_question(self) -> None:
        """Nicely print text of the question with possible answeres."""
        print(f"Question: {self.text}")  # noqa: T201
        answers = [opt.answer for opt in self.options]
        for letter, opt in zip(string.ascii_letters, answers, strict=False):
            print(f"\t{letter}) {opt}")  # noqa: T201


class Quiz(BaseModel):
    """Collection of questions with iteration state."""

    name: str
    questions: list[Question] = Field(default_factory=list)
    current_question: int = -1

    def __next__(self) -> Question:
        """Return the next question or raise StopIteration."""
        self.current_question += 1
        try:
            question = self.questions[self.current_question]
        except IndexError as exc:
            raise StopIteration from exc

        return question

    def __len__(self) -> int:
        """Return the number of questions in the quiz."""
        return len(self.questions)

    @property
    def question(self) -> Question:
        """Return the current question."""
        return self.questions[self.current_question]
