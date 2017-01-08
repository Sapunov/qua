from django.urls import reverse

from qua.api.models import Questions, SearchHistory
from qua import utils


class CategoryAssumptions:
    def __init__(self):
        self.assumptions = []

    def __iter__(self):
        return iter(self.assumptions)

    def __getitem__(self, key):
        return self.assumptions[key]

    def __len__(self):
        return len(self.assumptions)


class SearchHit:
    def __init__(self, id, title, categories, search_history_id,
        snippet=None, score=1.0, image=None
    ):
        self.id = id
        self.title = title
        self.categories = categories
        self.snippet = snippet or self.title
        self.score = score
        self.image = image
        self.url = self.make_tracker_url(search_history_id)

    def __str__(self):
        return '<SearchHit:{0:.30}|{1}>'.format(self.title, self.score)

    def __repr__(self):
        return self.__str__()

    def make_tracker_url(self, search_history_id):
        return '{0}?shid={1}&qid={2}&redirect={3}&token={4}'.format(
            reverse('tracker-search'), search_history_id, self.id,
            reverse('api-question', kwargs={'question_id': self.id}),
            utils.sign('{0}-{1}'.format(search_history_id, self.id))
            )


def make_assumptions(query):
    return CategoryAssumptions()


class SearchResults:
    def __init__(self, query, queryset, search_history_id):
        self.query = query
        self.total = queryset.count()
        self.hits = []
        self.category_assumptions = None

        if self.total > 0:
            for result in queryset:
                self.hits.append(
                    SearchHit(result.id, result.title, result.categories,
                        search_history_id))
        else:
            self.category_assumptions = make_assumptions(query)

    def __str__(self):
        return '<SearchResults:{0:.30}|{1}>'.format(self.query, self.total)

    def __repr__(self):
        return self.__str__()


def search(query, user, category=None):
    results = Questions.objects.filter(title__contains=query)

    if category is not None:
        results.filter(categories__id=category)

    history_record = SearchHistory.objects.create(
        query=query, user=user, results=results.count())

    return SearchResults(query, results, history_record.id)
