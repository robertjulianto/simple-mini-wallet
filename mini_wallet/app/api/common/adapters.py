import os
import re
from contextlib import contextmanager
from typing import ContextManager, no_type_check

from injector import inject
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, Session, make_transient, scoped_session

from mini_wallet.core.common.exceptions import EntityAlreadyExistsException
from mini_wallet.core.common.port.logger import ILogger
from mini_wallet.infrastructure.sqlalchemy.ports import ISessionManager


class SessionManager(ISessionManager):

    @inject
    def __init__(
            self,
            logger: ILogger
    ):
        env = os.getenv('APP_ENV')
        echo = env == 'local'
        self.engine = create_engine('postgresql://postgres:postgrespassword@localhost/mini_wallet', echo=echo)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
        self.logger = logger

    def get_session_scope(self) -> ContextManager[Session]:
        @no_type_check
        @contextmanager
        def thread_local_session_scope() -> ContextManager[Session]:
            session = self.Session()
            try:
                yield session
                # make all objects inside this session transient
                instances = session.identity_map.values() + list(session.new)
                for instance in instances:
                    make_transient(instance)
            except IntegrityError as e:
                error_message = e.orig.diag.message_detail
                key = re.search("Key (.+?)=(.+?) already exists.", error_message)
                session.rollback()
                raise EntityAlreadyExistsException(
                    entity=e.orig.diag.table_name.capitalize(),
                    entity_id_name=key.group(1).replace("_", " "),
                    entity_id=key.group(2).replace("_", " ")
                )
            except Exception as e:
                session.rollback()
                self.logger.error("Session Failed!", e)
                raise e
            finally:
                self.Session.remove()

        return thread_local_session_scope()
