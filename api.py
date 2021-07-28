import httpx
from fastapi import APIRouter, Query

from redis import cache
from const import FilterType


router = APIRouter()


@router.get('/ad')
async def get_ad(
    *,
    sdk_version: str = Query(None, alias='SDK Version'),
    username: str = Query(None, alias='User name'),
    # session_id: str = Query(None, alias='SessionId'),
    # platform: str = Query(None, alias='Platform'),
    # country_code: str = Query(None, alias='Country code'),
):
    async with httpx.AsyncClient() as client:
        resp = await client.get('https://6u3td6zfza.execute-api.us-east-2.amazonaws.com/prod/ad/vast')
        await cache.hincrby('ad-user-requests', username)
        await cache.hincrby('ad-sdk-requests', sdk_version)
        return resp.text


@router.post('/impression')
async def impression(
    *,
    sdk_version: str = Query(None, alias='SDK Version'),
    username: str = Query(None, alias='User name'),
):
    await cache.hincrby('impression-users', username)
    await cache.hincrby('impression-sdk', sdk_version)


@router.get('/stats')
async def stats(
    *,
    filter_type: str = Query(None, alias='FilterType')
):
    if filter_type == FilterType.SDK_VERSION:
        requests = await cache.hgetall('ad-sdk-requests')
        impressions = await cache.hgetall('impression-sdk')
    elif filter_type == FilterType.USERNAME:
        requests = await cache.hgetall('ad-user-requests')
        impressions = await cache.hgetall('impression-users')
    else:
        return
    fill_rate = {}
    usernames = requests.keys() | impressions.keys()
    for username in usernames:
        impression_count = int(impressions.get(username, 0))
        req_count = int(requests.get(username, 0))
        fill_rate[username] = impression_count / req_count if req_count != 0 else 0
    return {
        'requests': requests,
        'impressions': impressions,
        'fill_rate': fill_rate,
    }
