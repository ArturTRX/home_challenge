from fastapi.testclient import TestClient

from main import app
from const import ParamAlias, FilterType


TEST_SDK_VERSION = 'TEST SDK VERSION'
TEST_USERNAME = 'TEST USERNAME'

TEST_SDK_USERNAME_PARAMS_SET = [
    {ParamAlias.SDK_VERSION: TEST_SDK_VERSION, ParamAlias.USERNAME: TEST_USERNAME},
]

TEST_STATS_PARAMS_SET = [
    {ParamAlias.FILTER_TYPE: FilterType.SDK_VERSION},
    {ParamAlias.FILTER_TYPE: FilterType.USERNAME},
]

INVALID_SDK_USERNAMES_PARAMS_SET = [
    {},
    {ParamAlias.SDK_VERSION: TEST_SDK_VERSION},
    {ParamAlias.USERNAME: TEST_USERNAME},
    {'Test': 'test'},

    {ParamAlias.SDK_VERSION: ''},
    {ParamAlias.USERNAME: ''},
    {ParamAlias.SDK_VERSION: '', ParamAlias.USERNAME: TEST_USERNAME},
    {ParamAlias.SDK_VERSION: TEST_SDK_VERSION, ParamAlias.USERNAME: ''},

    {ParamAlias.SDK_VERSION: None},
    {ParamAlias.USERNAME: None},
    {ParamAlias.SDK_VERSION: None, ParamAlias.USERNAME: TEST_USERNAME},
    {ParamAlias.SDK_VERSION: TEST_SDK_VERSION, ParamAlias.USERNAME: None},
]


INVALID_STATS_PARAMS_SET = [
    {},
    {'Test': 'test'},
    {ParamAlias.FILTER_TYPE: ''},
    {ParamAlias.FILTER_TYPE: None},
    {ParamAlias.FILTER_TYPE: 'Test'}
]


def test_get_ad():
    with TestClient(app) as client:
        for params in TEST_SDK_USERNAME_PARAMS_SET:
            response = client.get('/api/ad/', params=params)
            assert response.status_code == 200


def test_get_ad_invalid_params():
    with TestClient(app) as client:
        for params in INVALID_SDK_USERNAMES_PARAMS_SET:
            response = client.get('/api/ad/', params=params)
            assert response.status_code == 422


def test_impression():
    with TestClient(app) as client:
        for params in TEST_SDK_USERNAME_PARAMS_SET:
            response = client.post('/api/impression/', json=params)
            assert response.status_code == 200


def test_impression_invalid_params():
    with TestClient(app) as client:
        for params in INVALID_SDK_USERNAMES_PARAMS_SET:
            response = client.post('/api/impression/', json=params)
            assert response.status_code == 422


def test_get_stats():
    with TestClient(app) as client:
        for params in TEST_STATS_PARAMS_SET:
            response = client.get('/api/stats/', params=params)
            assert response.status_code == 200
            assert response.json().keys() == {'requests', 'impressions', 'fill_rate'}


def test_get_stats_invalid_params():
    with TestClient(app) as client:
        for params in INVALID_STATS_PARAMS_SET:
            response = client.post('/api/impression/', json=params)
            assert response.status_code == 422
