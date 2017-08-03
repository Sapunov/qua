'''QUA blender
'''

from aiohttp import ClientSession
from collections import defaultdict
from requests.compat import urljoin
import aiohttp
import asyncio
import logging
import time

from django.conf import settings

from api import constants
from api import misc


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

def _scale_score(score, min_score, max_score):

    try:
        return (score - min_score) / (max_score - min_score)
    except ZeroDivisionError:
        return 0


def _scale_hits_scores(hits, min_score, max_score):

    for hit in hits:
        hit['_score'] = _scale_score(hit['_score'], min_score, max_score)


def _ensure_hit_location(hit):

    if not '_loc' in hit:
        hit['_loc'] = constants.SERP_MIDDLE_BLOCK


def merge_results(list_of_results):

    # If service cannot return anything `list_of_results` may contain None
    list_of_results = [it for it in list_of_results if it is not None]

    hits = []
    total = 0
    suggested_query = None

    locations = defaultdict(lambda: [])
    locations_count = defaultdict(lambda: 0)
    loc_sizes = {
        constants.SERP_MIDDLE_BLOCK: settings.SERP_MIDDLE_BLOCK_SIZE,
        constants.SERP_TOP_BLOCK: settings.SERP_TOP_BLOCK_SIZE,
        constants.SERP_RIGHT_BLOCK: settings.SERP_RIGHT_BLOCK_SIZE
    }

    for service, result in list_of_results:
        _scale_hits_scores(result['hits'], result['min_score'], result['max_score'])

        # Distribute all hits on 3 heaps by location
        for hit in result['hits']:
            _ensure_hit_location(hit)
            locations[hit['_loc']].append(hit)

        # Make some usefull staff
        if service == settings.MAIN_SEARCH_SERVICE_NAME and result['total'] > 0:
            # Search engine blend corrected queries to the query and already
            # shows results respect to suggests. But if no results found than
            # suggests is unusable
            suggested_query = result['suggested_query']

        total += result['total']

    # Sort all 3 heaps
    for key in locations.keys():
        locations[key].sort(key=lambda hit: hit['_score'], reverse=True)

    # And make one hits list with only specific number of each location
    for key in locations.keys():
        for hit in locations[key]:
            if locations_count[hit['_loc']] < loc_sizes[hit['_loc']]:
                hits.append(hit)
                locations_count[hit['_loc']] += 1
            # else do nothing

    ans = {
        'hits': hits,
        'suggested_query': suggested_query,
        'total': total
    }

    return ans


def search_async(query, limit, offset):

    search_providers = [name for name in settings.SERVICES['search'].keys()]
    # TODO: When merging results from different services we show only
    # specific amount of them because of page items limit. Consequently
    # some number of results from services remain unshown. What we need to do
    # is to save number of unshown results for specific service and when user
    # will make a query with the same terms and another limits show unshown
    # results with respect to page blocks limits.
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

    _start = time.time()

    results = eloop.run_until_complete(
        asyncio.ensure_future(_search_async(name_url))
    )

    ans = {'query': query, 'took': misc.time_elapsed(_start)}

    log.debug('Have a results from blender: %s', results)

    # Adding hits, suggested_query and hits
    ans.update(merge_results(results))

    return ans
