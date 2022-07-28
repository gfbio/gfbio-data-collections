import sys
import pytest

from collection_service.users.models import Service, User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"

def test_service():
    svc = Service(origin="gfbio:service")
    assert "gfbio:service" == f"{svc}"

def test_service():
    svc = Service(origin="gfbio#service")
    try:
        svc.clean()
        assert False
    except:
        assert sys.exc_info()[0].__name__ == "ValidationError"
