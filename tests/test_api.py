import httpx
import pytest

from app import client as yv_client


def test_votd_happy_path(client, mocker):
    mocker.patch.object(yv_client, "get_passage_id", return_value="REV.3.20")
    mocker.patch.object(
        yv_client,
        "get_passage_text",
        return_value={"id": "REV.3.20", "content": "Behold...", "reference": "Revelation 3:20"},
    )

    response = client.get("/votd", params={"day": 195, "version": 206})

    assert response.status_code == 200
    assert response.json() == {
        "day": 195,
        "reference": "Revelation 3:20",
        "text": "Behold...",
        "version_id": 206,
    }


@pytest.mark.parametrize("day", [0, 367, "abc"])
def test_invalid_day_returns_400(client, day):
    response = client.get("/votd", params={"day": day, "version": 206})

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_DAY"


def test_upstream_failure_returns_502(client, mocker):
    mocker.patch.object(yv_client, "get_passage_id", side_effect=httpx.ConnectError("boom"))

    response = client.get("/votd", params={"day": 195, "version": 206})

    assert response.status_code == 502
    assert response.json()["error"]["code"] == "UPSTREAM_ERROR"


def test_repeated_request_uses_cache(client, mocker):
    passage_id_mock = mocker.patch.object(yv_client, "get_passage_id", return_value="REV.3.20")
    passage_text_mock = mocker.patch.object(
        yv_client,
        "get_passage_text",
        return_value={"id": "REV.3.20", "content": "Behold...", "reference": "Revelation 3:20"},
    )

    client.get("/votd", params={"day": 195, "version": 206})
    client.get("/votd", params={"day": 195, "version": 206})

    assert passage_id_mock.call_count == 1
    assert passage_text_mock.call_count == 1