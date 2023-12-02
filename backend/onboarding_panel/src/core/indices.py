from pydantic_settings import BaseSettings

from .config import ELASTIC_INDICES
from src.models.message import QARecord, QARecordModelFilter, QARecordModelSort


class OnboardingPanelIndex(BaseSettings):
    INDEX: str = ELASTIC_INDICES.ONBOARDING_PANEL
    MODEL: type = QARecord
    SEARCH_FIELDS: list[str] = ['question.message', 'answer.message^2']
    MODEL_SORT: type = QARecordModelSort
    MODEL_FILTER: type = QARecordModelFilter


ONBOARDING_PANEL_INDEX = OnboardingPanelIndex()
