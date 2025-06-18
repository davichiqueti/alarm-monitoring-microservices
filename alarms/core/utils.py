import os
import requests


def check_user(user_id: int) -> bool:
    res = requests.get(f"{os.environ['USERS_APP_URL']}/users/{user_id}/")
    return res.status_code == 200
