# implement BM25 algorithm
from corpus_indexer import CorpusIndexer
import math
import argparse

class RankingBM25:
  def __init__(self, collection):
    self.collection = collection

    sum_of_length_of_clean_tokens = 0
    for doc in self.collection.documents:
      sum_of_length_of_clean_tokens += len(doc['clean_tokens'])

    # average document length (after tokens cleaning)
    self.avgdl = sum_of_length_of_clean_tokens / len(self.collection.documents)

  def query(self, query):
    clean_query_tokens = self.collection.clean_tokens(query.split())
       
    bm25_array = []
    for doc in self.collection.documents:
      total_score = sum(self.calculate_bm25(doc['clean_tokens'], query_token) for query_token in clean_query_tokens)
      bm25_array.append({ int(doc['docno']): total_score })
      bm25_array.sort(key=lambda x: list(x.values())[0], reverse=True)
    return bm25_array
  
  #  Calculate Probability Estimation
  # https://www.futurelearn.com/courses/mechanics-of-search-text-and-web-retrieval/4/steps/1866845
  # https://www.elastic.co/blog/practical-bm25-part-3-considerations-for-picking-b-and-k1-in-elasticsearch
    # 1.2 < k1 < 2   => 1.25
    # 0.5 < b < 0.8 => 0.75
  def calculate_bm25(self, document_term_vector, word, k=1.25, b=0.75):
    N = len(self.collection.documents)
    n = sum(doc['clean_tokens'].count(word) for doc in self.collection.documents)
    avgdl = self.avgdl
    tf = document_term_vector.count(word)

    idf = math.log(((N - n + 0.5) / (n + 0.5)) + 1)
    
    return round(tf/(tf + k*(1-b)+b*(N/avgdl)) * idf, 4)

if __name__ == "__main__":
  print("===================================================")
  print("Search Engine - Vector Space Model")
  print("===================================================")
  print("Author: Emerson Takeshi Urushibata")


  parser=argparse.ArgumentParser(description="sample argument parser")
  parser.add_argument("keywords", help="Search Keywords")
  args=parser.parse_args()

  # for testing purpose, define the collection size
  # limit = 1000 # any number or None
  limit = None
  collection = CorpusIndexer('./dataset/0.wikipedia.images.xml', limit)
  ranking_bm25 = RankingBM25(collection)
  
  similarity = ranking_bm25.query(args.keywords)
  print(f"Searching for {args.keywords}")
  print("===================================================")
  print("Results:")
  print(similarity)

