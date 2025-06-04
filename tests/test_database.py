import pytest

pytest.importorskip("sqlalchemy")

from ivi.database import create_db, User, Interaction


def test_create_user_interaction():
    Session = create_db("sqlite:///:memory:")
    session = Session()
    user = User(name="alice")
    session.add(user)
    session.commit()
    inter = Interaction(user=user, idea_id="idea1", description="x")
    session.add(inter)
    session.commit()
    assert session.query(User).count() == 1
    assert session.query(Interaction).count() == 1
    session.close()
