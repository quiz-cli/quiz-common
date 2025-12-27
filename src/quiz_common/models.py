from dataclasses import dataclass, field


@dataclass
class Option:
    answer: str
    correct: bool


@dataclass
class Question:
    text: str
    time_limit: int | None = None
    options: list[Option] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.options = [Option(**opt) for opt in self.options] # pyright: ignore[reportCallIssue]

    def ask(self) -> dict:
        return {
            "type": "question",
            "text": self.text,
            "options": [opt.answer for opt in self.options],
        }


@dataclass
class Quiz:
    name: str
    questions: list[Question] = field(default_factory=list)
    current_question: int = -1

    def __post_init__(self):
        self.questions = [Question(**q) for q in self.questions] # pyright: ignore[reportCallIssue]

    def __next__(self) -> Question:
        self.current_question += 1
        try:
            question = self.questions[self.current_question]
        except IndexError:
            raise StopIteration

        return question

    def __len__(self) -> int:
        return len(self.questions)

    @property
    def question(self):
        return self.questions[self.current_question]
