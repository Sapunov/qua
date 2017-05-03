from qua.elasticsearch import Elasticsearch
from qua import settings


def boolean_query(query_body, policy='should', query_type='match'):

    clause = []

    for key, values in query_body.items():
        if isinstance(values, (list, tuple, set)):
            for value in values:
                clause.append({
                    query_type: {
                        key: value
                    }
                })
        else:
            clause.append({
                query_type: {
                    key: values
                }
            })

    return { policy: clause }


def query(index, doc_type, body, **kwargs):

    client = Elasticsearch()

    if 'size' in kwargs and kwargs['size'] > settings.MAX_SEARCH_RESULTS:
        kwargs['size'] = settings.MAX_SEARCH_RESULTS
    elif 'size' not in kwargs:
        kwargs['size'] = settings.MAX_SEARCH_RESULTS


    results = client.search(
        index=index,
        doc_type=doc_type,
        body=body, **kwargs)

    took = round(results['took'] / 1000, 3)
    total = results['hits']['total']

    if total > 0:
        out_results = [
            (res['_score'], res['_source']) for res in results['hits']['hits']
        ]
    else:
        out_results = None

    return (total, took, out_results)
