import httpx
from fastapi import APIRouter, Query, HTTPException, Body

from redis import cache
from const import FilterType, ParamAlias, CacheHashKey


router = APIRouter()


@router.get('/ad')
async def get_ad(
    *,
    sdk_version: str = Query(None, alias=ParamAlias.SDK_VERSION, min_length=1),
    username: str = Query(None, alias=ParamAlias.USERNAME, min_length=1),
    # session_id: str = Query(None, alias='SessionId'),
    # platform: str = Query(None, alias='Platform'),
    # country_code: str = Query(None, alias='Country code'),
):
    if sdk_version is None or username is None:
        raise HTTPException(status_code=422)
    async with httpx.AsyncClient() as client:
        resp = await client.get('https://6u3td6zfza.execute-api.us-east-2.amazonaws.com/prod/ad/vast')
        await cache.hincrby(CacheHashKey.AD_USER_REQUESTS, username)
        await cache.hincrby(CacheHashKey.AD_SDK_REQUESTS, sdk_version)
        return resp.text


@router.post('/impression/')
async def impression(
    *,
    sdk_version: str = Body(None, alias=ParamAlias.SDK_VERSION, min_length=1),
    username: str = Body(None, alias=ParamAlias.USERNAME, min_length=1),
):
    if sdk_version is None or username is None:
        raise HTTPException(status_code=422)
    await cache.hincrby(CacheHashKey.USER_IMPRESSIONS, username)
    await cache.hincrby(CacheHashKey.SDK_IMPRESSIONS, sdk_version)


@router.get('/stats')
async def stats(
    *,
    filter_type: str = Query(None, alias=ParamAlias.FILTER_TYPE)
):
    if filter_type == FilterType.SDK_VERSION:
        requests = await cache.hgetall(CacheHashKey.AD_SDK_REQUESTS)
        impressions = await cache.hgetall(CacheHashKey.USER_IMPRESSIONS)
    elif filter_type == FilterType.USERNAME:
        requests = await cache.hgetall(CacheHashKey.AD_USER_REQUESTS)
        impressions = await cache.hgetall(CacheHashKey.USER_IMPRESSIONS)
    else:
        raise HTTPException(status_code=422)
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
