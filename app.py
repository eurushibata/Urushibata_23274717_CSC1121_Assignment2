#!/usr/bin/env python
from flask import Flask, render_template, send_from_directory, Response, json
import os
from ranking_bm25 import RankingBM25
from ranking_vsm import RankingVSM
from ranking_vsm_q import RankingVSM_Q
from corpus_indexer import CorpusIndexer
from multiprocessing import Pool

app = Flask(__name__,
             template_folder='web/dcu.ca2/webapp')

def initialize_rankings():
  print("Rankings initialized")
  global ranking_bm25, ranking_vsm, ranking_vsm_q  # Declare as global to modify them
  collection = CorpusIndexer('./dataset/0.wikipedia.images.xml')

  ranking_bm25 = RankingBM25(collection)
  ranking_vsm = RankingVSM(collection)
  ranking_vsm_q = RankingVSM_Q(collection)
  print("Rankings finished loading")

@app.route("/")
def hello():
  message = "Hello, World"
  return render_template("index-cdn.html", message=message)

@app.route("/search/<algo>/<query>")

def search(algo, query):
  ranking = None

  if (algo == "bm25"):
    ranking = ranking_bm25.query(query)
  elif (algo == "vsm"):
    ranking = ranking_vsm.query(query)
  elif (algo == "vsm_q"):
    ranking = ranking_vsm_q.query(query)

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

@app.route("/dataset")
def dataset():
    dataset_path = os.path.join(app.root_path, 'dataset/0.wikipedia.images.json')
    try:
        with open(dataset_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # Load JSON content
        return app.response_class(
            response=json.dumps(data, indent=2, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )
    except FileNotFoundError:
        return Response(
            "Dataset file not found",
            status=404,
            mimetype='text/plain'
        )


@app.route('/<path:filename>')
def serve_static_file(filename):
    static_dir = os.path.join(app.root_path, 'web/dcu.ca2/webapp')
    return send_from_directory(static_dir, filename)

def initialize_ranking(args):
    ranking_class, collection = args
    return ranking_class(collection)

initialize_rankings()

# it is ignored by gunicorn
if __name__ == "__main__":
  app.run(debug=True, port=8000)