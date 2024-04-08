import pytest
@pytest.mark.parametrize(
    "path, expected_status, expected_response",
    [
        pytest.param("/items", 200, {"q": None, "skip": 0, "limit": 100}, id="test_get"),
        pytest.param("/items?q=foo", 200, {"q": "foo", "skip": 0, "limit": 100}, id="test_get"),
        pytest.param(
            "/items?q=foo&skip=5", 200, {"q": "foo", "skip": 5, "limit": 100}, id="test_get"
        ),
        pytest.param(
            "/items?q=foo&skip=5&limit=30", 200, {"q": "foo", "skip": 5, "limit": 30}, id="test_get"
        ),
        pytest.param("/users", 200, {"q": None, "skip": 0, "limit": 100}, id="test_get"),
        pytest.param("/items", 200, {"q": None, "skip": 0, "limit": 100}, id="test_get"),
        pytest.param("/items?q=foo", 200, {"q": "foo", "skip": 0, "limit": 100}, id="test_get"),
        pytest.param(
            "/items?q=foo&skip=5", 200, {"q": "foo", "skip": 5, "limit": 100}, id="test_get"
        ),
        pytest.param(
            "/items?q=foo&skip=5&limit=30", 200, {"q": "foo", "skip": 5, "limit": 30}, id="test_get"
        ),
        pytest.param("/users", 200, {"q": None, "skip": 0, "limit": 100}, id="test_get"),
    ],
)
def test_get_parametrized(client: TestClient, path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


