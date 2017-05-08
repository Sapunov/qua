import pickle

from django.conf import settings

from suggests import models
from suggests.tst import TernarySearchTree


def _preprocess(item):
    '''Preprocess input data
    Input: AccumulateQueue object
    Returns tuple: (query, last, freq, quick_answer)
    '''

    conf = settings.SUGGEST_PREPROCESSOR

    query = item.text
    last = item.last
    freq = item.freq
    quick_answer = item.quick_ans

    if len(query) < conf['min_query_len'] or last > conf['max_last']:
        raise ValueError

    query = query.lower().strip()

    if quick_answer:
        quick_answer = quick_answer.lower().strip()

    # Replace some substrings
    for pattern, to in conf['replacements']:
        query = query.replace(pattern, to)

    # Normalize whitespaces
    query = ' '.join(word.strip() for word in query.split(' '))

    return (query, last, freq, quick_answer)


def _get_queries(data):
    '''Transform data dict to length sorted list of tuples with queries only
    '''

    return sorted(
        [it for it in data.keys()], key=lambda it: len(it), reverse=True)


def _add_node(root, string):

    for it in root:
        if it[0].startswith(string):
            _add_node(it[1], string)
            break
    else:
        root.append([string, []])


def _create_tree(queries):
    '''Nesting tree.
    With help of it we can remove nested mistakan queries.
    For example: 'zabbix' and 'zabb' -> 'zabb' will be removed
    '''

    root = []
    for query in queries:
        _add_node(root, query)

    return root


def _data_pruning(tree, data, stack=[]):
    '''Remove mistakan queries from data

    Attention: this function works with data dict INPLACE
    '''

    for node in tree:
        stack.append(node[0])
        if node[1]:
            _data_pruning(node[1], data, stack)

        current = stack.pop()
        # Delete data if ancestor has more words
        # Don't delete if data has quick_answer
        if len(stack) and data[current][1] is None \
                and len(stack[-1].split(' ')) == len(current.split(' ')):
            del data[current]


def _load_group_data(group_id):

    data = {}
    to_process = models.AccumulateQueue.objects.filter(
        processed=False, group_id=group_id)

    if to_process.count() == 0:
        return []

    for item in to_process:
        try:
            query, last, freq, quick_answer = _preprocess(item)
        except ValueError:
            continue

        if query not in data:
            data[query] = [freq, last, quick_answer]
        else:
            data[query][0] += 1

            # Min last matters
            if data[query][1] < last:
                data[query][1] = last

    # Calculating rating
    # rate = floor((freq / last) * 1000)
    for key, value in data.items():
        data[key] = (int(value[0] / value[1] * 1000), value[2])

    # Set items as processed
    to_process.update(processed=True)

    return data


def _get_unique_groups():

    qset = models.AccumulateQueue.objects.filter(
        processed=False).values_list('group_id').distinct()

    return [item[0] for item in qset]


def preprocess():

    overall = []

    for group_id in _get_unique_groups():

        data = _load_group_data(group_id)
        tree = _create_tree(_get_queries(data))
        _data_pruning(tree, data)

        for key, value in data.items():
            overall.append((key, *value))  # (query, last, quick_ans)

    return overall


def create_tst():

    data = preprocess()

    if not data:
        return None

    tst = TernarySearchTree()

    for query, last, quick_ans in data:
        tst.insert(query, last, quick_ans)

    tst.optimize(common_num=settings.SUGGESTS_DEFAULT_LIMIT)

    # Save tree
    with open(settings.SUGGESTS_TREE_PATH, 'wb') as fd:
        pickle.dump(tst, fd)

    # Now we can delete processed data
    # models.AccumulateQueue.object.delete(processed=True)

    return tst
