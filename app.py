#!/usr/bin/env python
from flask import Flask, render_template, send_from_directory, Response, json
import os
from ranking_bm25 import RankingBM25
from ranking_vsm import RankingVSM
from corpus_indexer import CorpusIndexer

app = Flask(__name__,
             template_folder='web/dcu.ca2/webapp')

@app.route("/")
def hello():
  message = "Hello, World"
  return render_template("index-cdn.html", message=message)

@app.route("/search/<algo>/<query>")
def search(algo, query):
  collection = CorpusIndexer('./dataset/0.wikipedia.images.xml')
  ranking = None
  if (algo == "bm25"):
    ranking_bm25 = RankingBM25(collection)
    ranking = ranking_bm25.query(query)
  elif (algo == "vsm"):
    ranking_vsm = RankingVSM(collection)
    ranking = ranking_vsm.query(query)

  
  # print(ranking)
  if (ranking is None):
    return Response(
        "No ranking found",
        status=404,
        mimetype='text/plain'
    )
  response = app.response_class(
        response=json.dumps(ranking),
        status=200,
        mimetype='application/json'
    )
  
  return response


@app.route('/<path:filename>')
def serve_static_file(filename):
    static_dir = os.path.join(app.root_path, 'web/dcu.ca2/webapp')
    return send_from_directory(static_dir, filename)

if __name__ == "__main__":
  app.run(debug=True, port=8005)