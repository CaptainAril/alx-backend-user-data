#!/usr/bin/env python3
"""DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memorized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ Adds, saves and returns a new user added to the database.
        """
        usr = User(email=email, hashed_password=hashed_password)
        sess = self._session
        sess.add(usr)
        sess.commit()
        return usr

    def find_user_by(self, **kwargs) -> User:
        """Returns first user matching query parameter `kwargs`.
        """
        for k, v in kwargs.items():
            try:
                user = self._session.query(User)\
                    .filter(getattr(User, k) == v).first()
            except AttributeError:
                raise InvalidRequestError
        if user:
            return user
        else:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates User attributes by user_id.
        """
        query = {'id': user_id}
        user = self.find_user_by(**query)
        if user:
            for k, v in kwargs.items():
                setattr(user, k, v)
        return None
