from qua import celery
from qua.api.utils import index as index_util
from qua.api.models import Question
from qua.api.utils.common import get_text_from_html


@celery.app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@celery.app.task(bind=True)
def index_question(self, question_id):

    question = Question.get(question_id)

    if hasattr(question, 'keywords'):
        keywords = list(question.keywords.values_list('text', flat=True))
    else:
        keywords = []

    if hasattr(question, 'categories'):
        keywords.extend(list(question.categories.values_list('name', flat=True)))

    text = question.title + ' '

    if question.answer_exists:
        text += get_text_from_html(question.answer.html)

    data = {
        'id': question.id,
        'keywords': ','.join(keywords),
        'text': text
    }

    index_util.index(data)
