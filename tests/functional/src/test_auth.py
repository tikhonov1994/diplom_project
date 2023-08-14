import pytest

pytestmark = pytest.mark.asyncio



# todo test login success
async def test_login(http_client) -> None:
    login
    async with http_client.get(ENDPOINT + str(film_id)) as response:
        data = await response.json()

        assert response.status == HTTPStatus.OK
        assert data['id'] == film_id


# todo test login negative(wrong login or password)
