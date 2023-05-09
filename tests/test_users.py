from jose import jwt
from app import schemas
from .database import client, session
from app.config import settings


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello Dear World...!'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/api/users/create-user", json={
        "email": "hello1234@gmail.com",
        "password": "password1234"
    })
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello1234@gmail.com"
    assert res.status_code == 201


def test_login_user(client):
    res = client.post("/api/auth/login", data={
        "username":'hello1234@gmail.com',
        "password":'password1234'
    })
    print('%$#$%^%$%#$#^$^$%$#%@!#@!$@$%$%^$^&%^&%(^)*^&&', res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    # assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


# @pytest.mark.parametrize("email, password, status_code", [
#     ('wrongemail@gmail.com', 'password123', 403),
#     ('sanjeev@gmail.com', 'wrongpassword', 403),
#     ('wrongemail@gmail.com', 'wrongpassword', 403),
#     (None, 'password123', 422),
#     ('sanjeev@gmail.com', None, 422)
# ])
# def test_incorrect_login(test_user, client, email, password, status_code):
#     res = client.post(
#         "/login", data={"username": email, "password": password})
#     assert res.status_code == status_code
#     # assert res.json().get('detail') == 'Invalid Credentials'