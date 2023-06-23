from dataclasses import dataclass
from typing import List, Optional
import nltk

SPACE = ' '


def split_text_by_sentenses(text):
    tokens = nltk.sent_tokenize(text)

    return (token.strip() for token in tokens)


@dataclass
class ChunkSegments:
    prefix: str
    sentenses: List[str]
    postfix: Optional[str]

    def to_parts(self) -> List[str]:
        parts = []
        parts.append(self.prefix)
        for s in self.sentenses:
            parts.append(s)
        if self.postfix:
            parts.append(self.postfix)
        return parts

    def __str__(self) -> str:
        return SPACE.join(self.to_parts())

    def str_len(self) -> int:
        parts = self.to_parts()
        l = 0
        for part in parts:
            if isinstance(part, str):
                l += len(part)
            else:
                l += 1
        return l + (len(parts) - 1)


def split_text_to_chunks(
        text,
        max_length,
        answer_prefix,
        answer_postfix,
        first_answer_prefix,
):
    results: List[str] = []

    chunks_segments = ChunkSegments(
        prefix=first_answer_prefix,
        sentenses=[text],
        postfix=None,
    )

    if chunks_segments.str_len() > max_length:
        sentenses = list(split_text_by_sentenses(text))
        prefix = first_answer_prefix
        chunk_sentenses = []
        k = 0
        while k < len(sentenses):
            sentense = sentenses[k]
            k += 1
            chunk_sentenses.append(sentense)

            chunks_segments = ChunkSegments(
                prefix=prefix,
                sentenses=chunk_sentenses,
                postfix=answer_postfix,
            )
            if chunks_segments.str_len() <= max_length:
                continue

            chunk_sentenses.pop()

            if chunk_sentenses:
                results.append(
                    str(ChunkSegments(
                        prefix=prefix,
                        sentenses=chunk_sentenses,
                        postfix=answer_postfix,
                    ))
                )
                prefix = answer_prefix
                chunk_sentenses = []
                k -= 1
                continue

            words = []
            words += sentense.split(SPACE)

            i = 0
            word_list = []
            while i < len(words):
                word = words[i]
                i += 1
                word_list.append(word)

                chunk_segments = ChunkSegments(
                    prefix=prefix,
                    sentenses=word_list,
                    postfix=answer_postfix,
                )
                if chunk_segments.str_len() < max_length:
                    continue

                word_list.pop()
                results.append(
                    str(ChunkSegments(
                        prefix=prefix,
                        sentenses=word_list,
                        postfix=answer_postfix,
                    ))
                )
                prefix = answer_prefix
                i -= 1
                word_list = []

            if k == len(sentenses):
                postfix = None
            else:
                postfix = answer_postfix
            if word_list:
                results.append(
                    str(ChunkSegments(
                        prefix=prefix,
                        sentenses=word_list,
                        postfix=postfix,
                    ))
                )

        if chunk_sentenses:
            chunks_segments = ChunkSegments(
                prefix=prefix,
                sentenses=chunk_sentenses,
                postfix=None
            )
            results.append(str(chunks_segments))
    else:
        results = [str(chunks_segments)]
    return results
