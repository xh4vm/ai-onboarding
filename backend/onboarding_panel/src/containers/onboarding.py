from dependency_injector import containers, providers

from ..db.base import Database
from .base import BaseContainer
from ..services.question import QuestionService
from ..repositories.question import QuestionRepository
from ..services.answer import AnswerService
from ..repositories.answer import AnswerRepository


class ServiceContainer(BaseContainer):

    wiring_config = containers.WiringConfiguration(modules=['..api.v1.chat'])

    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=config.db.url)

    question_repository = providers.Factory(
        QuestionRepository,
        session_factory=db.provided.session,
    )

    question_service = providers.Factory(
        QuestionService,
        question_repository=question_repository,
    )

    answer_repository = providers.Factory(
        AnswerRepository,
        session_factory=db.provided.session,
    )

    answer_service = providers.Factory(
        AnswerService,
        answer_repository=answer_repository,
    )
