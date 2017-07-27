from aiohttp import ClientSession
from requests.compat import urljoin
import aiohttp
import asyncio
import logging

from django.conf import settings

from qua import misc


log = logging.getLogger(settings.APP_NAME + __name__)


async def _fetch(name, url, session):

    try:
        async with session.get(url) as response:
            if response.status == 200:
                return (name, await response.json())
            else:
                raise aiohttp.client_exceptions.ClientError(
                    'GET query to `{0}` returns status_code={1}'.format(
                        url, response.status
                    )
                )
    except aiohttp.client_exceptions.ClientError as exc:
        log.error('Exception `%s` occurs while requesting %s', exc, url)


async def _search_async(name_url):

    tasks = []

    async with ClientSession() as session:
        for name, url in name_url:
            tasks.append(asyncio.ensure_future(_fetch(name, url, session)))

        return await asyncio.gather(*tasks)


def merge_results(list_of_results):

    # result - (name, service_response)

    return list_of_results


def search_async(query, limit, offset):

    search_providers = [name for name in settings.SERVICES['search'].keys()]
    query_string = misc.create_query({
        'query': query,
        'limit': limit,
        'offset': offset
    })

    query_string = 'search?' + query_string

    name_url = [(name, urljoin(
            settings.SERVICES['search'][name]['host'], query_string
        )) for name in search_providers]

    eloop = asyncio.get_event_loop()

    results = eloop.run_until_complete(
        asyncio.ensure_future(_search_async(name_url))
    )

    return merge_results(results)
