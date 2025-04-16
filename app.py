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

if __name__ == "__main__":
  processes_pool = Pool(5)
  # read files and prepare structure for engine optimization
  collection = CorpusIndexer('./dataset/0.wikipedia.images.xml')

  # Create a pool of processes
  ranking_classes = [RankingBM25, RankingVSM, RankingVSM_Q]
  args = [(cls, collection) for cls in ranking_classes]
  rankings = processes_pool.map(initialize_ranking, args)

  ranking_bm25, ranking_vsm, ranking_vsm_q = rankings


  app.run(debug=True, port=8005)