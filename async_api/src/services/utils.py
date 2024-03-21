from typing import Any
from elasticsearch_dsl import Search, Q
from db.elastic import get_elastic


def get_key_by_args(*args: Any, **kwargs: Any) -> str:
    return f"{args}:{kwargs}"


def get_elasticsearch_dict(index, query_params):
    s = Search(using=get_elastic(), index=index)
    query = Q("match", **query_params)
    s = s.query(query)
    response = s.execute()
    return response.to_dict()
