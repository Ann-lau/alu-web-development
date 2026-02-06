#!/usr/bin/env python3
"""Test client for Flask API using requests"""

import requests

BASE_URL = "http://127.0.0.1:5000"  # Change if your app runs elsewhere


def register_user(email: str, password: str) -> None:
    """Register a new user"""
    response = requests.post(f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 201 or response.status_code == 400
    if response.status_code == 201:
        assert response.json() == {"email": email, "message": "user created"}
    else:
        assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Try logging in with wrong password"""
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Login user and return session_id"""
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["message"] == "logged in"
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    return session_id


def profile_unlogged() -> None:
    """Access profile without logging in"""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Access profile with valid session"""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data


def log_out(session_id: str) -> None:
    """Logout user"""
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"message": "OK"}


def reset_password_token(email: str) -> str:
    """Request reset password token"""
    response = requests.post(f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert "reset_token" in data
    return data["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password using reset token"""
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email, "reset_token": reset_token, "new_password": new_password},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["message"] == "Password updated"


# ------------------------------
# Main test workflow
# ------------------------------
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
