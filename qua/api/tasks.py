from celery.utils.log import get_task_logger

from qua import celery
from qua.api.search import index
from qua.api.models import Question


log = get_task_logger(__name__)


@celery.app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

def _index_question(question):

    if hasattr(question, 'keywords'):
        keywords = list(question.keywords.values_list('text', flat=True))
    else:
        keywords = []

    if question.answer_exists:
        html = question.answer.html
    else:
        html = ''

    index.index_question(
        question_id=question.id,
        title=question.title,
        keywords=keywords,
        html=html
    )


@celery.app.task(bind=True)
def index_question(self, question_id):

    question = Question.get(question_id)

    _index_question(question)


@celery.app.task(bind=True)
def reindex_questions(self):

    questions = Question.objects.filter(deleted=False)

    for question in questions:
        _index_question(question)
