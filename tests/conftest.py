import pytest
from app import create_app
from app import db
from app.models.user_and_rec_models import User


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

# This fixture creates two users and saves them to the db
@pytest.fixture
def two_users_no_followers(app):
    new_user_1 = User(
        username="Lili Parra"
    )

    new_user_2 = User(
        username="Tyrah Gullette"
    )

    db.session.add(new_user_1)
    db.session.add(new_user_2)
    db.session.commit()