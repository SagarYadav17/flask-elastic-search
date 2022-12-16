from flask import Flask, request
from elasticsearch import Elasticsearch, NotFoundError
from os import environ


ES_ENDPOINT = environ.get("ES_ENDPOINT", "http://localhost:9200")

app = Flask(__name__)
es = Elasticsearch(hosts=[ES_ENDPOINT])


def es_search(index: str, body: dict):
    try:
        response = es.search(index=index, query=body).get("hits").get("hits")
    except NotFoundError:
        response = {}

    return response


@app.route("/")
def hello_geek():
    return "<h1>Hello There</h2>"


@app.route("/country/", methods=["GET"])
def search():
    body = {}
    keyword = request.args.get("search")

    if keyword:
        body = {"multi_match": {"query": keyword, "fields": ["name", "iso3"], "fuzziness": 2}}

    res = es_search(index="country", body=body)
    return res


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
