from sqlalchemy.orm.scoping import scoped_session


def add(*args, **kwargs):
    pass


def commit(*args, **kwargs):
    pass


class scoped_session(scoped_session):
    add: add
    commit: commit
