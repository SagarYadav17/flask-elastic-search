from flask import Flask, request
from elasticsearch import Elasticsearch, NotFoundError
from os import environ


ES_ENDPOINT = environ.get("ES_ENDPOINT", "http://elastic:12345678@localhost:9200")

app = Flask(__name__)
es = Elasticsearch(hosts=[ES_ENDPOINT])


def es_search(index: str, body: dict):
    try:
        response = es.search(index=index, body=body).get("hits").get("hits")
    except NotFoundError:
        response = {}

    return response


@app.route("/")
def hello_geek():
    return "<h1>Hello There</h2>"


@app.route("/country", methods=["GET"])
def search():
    body = {}
    keyword = request.args.get("search")

    if keyword:
        body = {"query": {"multi_match": {"query": keyword, "fields": ["name", "iso3"], "fuzziness": 2}}}

    res = es_search(index="country", body=body)
    return res


if __name__ == "__main__":
    app.run(port=5000, debug=True)
