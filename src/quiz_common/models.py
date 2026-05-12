"""Shared data models used by quiz components."""

from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Union, Literal, Optional

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

""" MESSAGE MODELS"""

class BasicMessage(BaseModel):
      """Base message model with a type field."""

      type: str
      #timestamp: Optional[float] = None

class TextMessage(BasicMessage):
    """Generic text message."""

    type: Literal["text"]
    text: str  
    params: Optional[dict[str, str]] = None

class QuestionMessage(BasicMessage):
    """Message sent by the server to present a question."""

    type: Literal["quiz_question"]
    question: Question

class AnswerMessage(BasicMessage):
    """Message sent by players to submit their answer."""

    type: Literal["quiz_answer"]
    client_id: str
    answer : list[bool] = Field(default_factory=list)

""" Discriminated union of all supported quiz message types."""
Message = Annotated [
    Union[QuestionMessage, AnswerMessage, TextMessage],
    Field(discriminator="type")
]

