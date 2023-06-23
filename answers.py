from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AnswerChunk:
    ready: bool
    text: Optional[str]
    last: bool



@dataclass
class Answer:
    ready: bool
    chunks: List[str]
    current_chunk: int

