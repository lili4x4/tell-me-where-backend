import pytest
from app.models.user import User

# def test_get_one_saved_user_no_followers(client, two_users_no_followers):
#     #Act
#     response = client.get("/users/1")
#     response_body = response.get_json()

#     #Assert
#     assert response.status_code == 200
#     assert "user" in response_body