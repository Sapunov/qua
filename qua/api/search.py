import logging

from django.urls import reverse

from qua.api.models import Question, SearchHistory
from qua import utils
from qua.api.utils import search as search_util


log = logging.getLogger('qua.' + __name__)


class CategoryAssumptions:
    def __init__(self):
        self.assumptions = []

    def __iter__(self):
        return iter(self.assumptions)

    def __getitem__(self, key):
        return self.assumptions[key]

    def __len__(self):
        return len(self.assumptions)


class UrlParams:
    def __init__(self, shid, qid, token):
        self.shid = shid
        self.qid = qid
        self.token = token
        self.track = 'search'


class SearchHit:
    def __init__(self, id, title, search_history_id,
        keywords=None, snippet=None, score=1.0, image=None
    ):
        self.id = id
        self.title = title
        self.snippet = snippet or self.title
        self.keywords = keywords
        self.score = score
        self.image = image
        self.url_params = self.get_url_params(search_history_id)

    def __str__(self):
        return '<SearchHit:{0:.30}|{1}>'.format(self.title, self.score)

    def __repr__(self):
        return self.__str__()

    def get_url_params(self, search_history_id):
        return UrlParams(
            search_history_id, self.id,
            utils.sign('{0}-{1}'.format(search_history_id, self.id))
        )


def make_assumptions(query):
    return CategoryAssumptions()


class SearchResults:
    def __init__(
        self, query, queryset=None, search_history_id=None, engine_answer=None
    ):
        self.query = query
        self.total = 0

        if queryset is not None:
            self.total = queryset.count()

        self.hits = []
        self.category_assumptions = None

        if self.total > 0:
            for result in queryset:
                self.hits.append(
                    SearchHit(
                        result.id,
                        result.title,
                        search_history_id,
                        keywords=result.keywords,
                        score=engine_answer[result.id]['score'],
                        snippet=engine_answer[result.id]['text'][:140]
                    )
                )

            self.hits.sort(key=lambda x: x.score, reverse=True)

        else:
            self.category_assumptions = make_assumptions(query)

    def __str__(self):
        return '<SearchResults:{0:.30}|{1}>'.format(self.query, self.total)

    def __repr__(self):
        return self.__str__()


def search(query, user):

    log.debug('Search for: %s', query)

    if query == '':
        return SearchResults(query)

    search_results = search_util.search(query)

    log.debug('Rearch results: %s' % search_results)

    results = Question.objects.filter(
        pk__in=search_results['hits'].keys(),
        deleted=False
    )

    history_record = SearchHistory.objects.create(
        query=query, user=user, results=results.count())

    return SearchResults(query, results, history_record.id, search_results['hits'])
