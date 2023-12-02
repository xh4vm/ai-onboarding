from .base import BaseService
from src.core.indices import ONBOARDING_PANEL_INDEX
from src.models.base import PageModel


class ChatMessageService(BaseService):
    index = ONBOARDING_PANEL_INDEX.INDEX
    model = ONBOARDING_PANEL_INDEX.MODEL
    search_fields = ONBOARDING_PANEL_INDEX.SEARCH_FIELDS
    model_sort = ONBOARDING_PANEL_INDEX.MODEL_SORT
    model_filter = ONBOARDING_PANEL_INDEX.MODEL_FILTER
