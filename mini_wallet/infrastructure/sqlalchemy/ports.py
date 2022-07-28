from abc import ABC, abstractmethod
from typing import ContextManager

from sqlalchemy.orm import Session


class ISessionManager(ABC):

    @abstractmethod
    def get_session_scope(self) -> ContextManager[Session]:
        raise NotImplementedError
