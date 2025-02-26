import httpx
from bs4 import BeautifulSoup


def get_login_client(username: str, password: str, login_url: str) -> httpx.Client:
    client = httpx.Client()
    resp = client.get(login_url).raise_for_status()
    form_build_id = (
        BeautifulSoup(resp.content, features="html.parser")
        .find("input", attrs={"name": "form_build_id"})
        .get("value")
    )
    payload = {
        "name": username,
        "pass": password,
        "form_build_id": form_build_id,
        "form_id": "user_login",
        "op": "Log in",
    }
    _ = client.post(login_url, data=payload, follow_redirects=True).raise_for_status()
    return client
