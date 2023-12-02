from typing import Iterator, Any

from loguru import logger
from src.transform.base import BaseTransformer
from src.models.qa_record import QARecord, Question, Answer


class QARecordTransformer(BaseTransformer):
    def transform(
        self, raw: Iterator[dict[str, Any]], to_dict: bool = False
    ) -> Iterator[Any]:
        
        for raw_elem in raw:
            question = Question(
                id=str(raw_elem.get("question_id")),
                user_id=str(raw_elem.get("question_user_id")),
                message=raw_elem.get("question_message"),
            )

            answer = Answer(
                id=str(raw_elem.get("answer_id")),
                question_id=str(raw_elem.get("answer_question_id")),
                message=raw_elem.get("answer_message"),
            ) if raw_elem.get("answer_id") is not None else None

            elem = QARecord(question=question, answer=answer)
            yield elem.model_dump(by_alias=True) if to_dict else elem
