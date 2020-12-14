import os
import tempfile

from app import app
from repository.sqlite_db import SQliteRepository


def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            repo = SQliteRepository()
            repo.init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])