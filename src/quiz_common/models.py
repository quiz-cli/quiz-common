"""Shared data models used by quiz components."""

from pydantic import BaseModel, Field


class Option(BaseModel):
    """Single answer option for a question."""

    answer: str
    correct: bool


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
            "options": [opt.answer for opt in self.options],
        }


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
