# implement ranking vector space model using cosine similarity (this variation only uses the terms present in the query)
from corpus_indexer import CorpusIndexer
from datetime import datetime
import argparse

class RankingVSM_Q:
  def __init__(self, collection):
    self.collection = collection
    self.document_term_matrix = None

    start_time = datetime.now()
    # print('STARTED: creating DOCUMENT-TERM matrix')
    self.document_term_matrix = collection.generate_document_term_matrix()
    # print(f'FINISHED ({(datetime.now() - start_time).total_seconds()} seconds)')
    # print(self.document_term_matrix)

  # Create Vector Space Model
  # https://www.futurelearn.com/courses/mechanics-of-search/4/steps/1866813
  # use the self.document_term_matrix to create the VSM
  def calculate_similarity(self, query):
    clean_query_tokens = self.collection.clean_tokens(query.split())

    query_vector = {}
    query_terms = []
    for term in clean_query_tokens:
      if term in query_vector:
        query_vector[term] += 1
      else:
        query_vector[term] = 1
        query_terms.append(term)
    # print(query_vector)

    # # to simplify the calculation, we can remove the terms that are not in the query
    clean_document_term_matrix = {}
    for docno, terms_index in self.document_term_matrix.items():
      clean_document_term_matrix[docno] = {}
      for term in query_terms:
        if term in terms_index:
          clean_document_term_matrix[docno][term] = terms_index[term]
      # print(clean_document_term_matrix)

    # calculate the cosine similarity
    similarity_all_documents = {}
    for docno, document_term_vector in clean_document_term_matrix.items():
      similarity_all_documents[docno] = self.cosine_similarity_per_document(query_vector, document_term_vector)
    return similarity_all_documents
  
  def cosine_similarity_per_document(self, query_vector, document_term_matrix):
    dot_product = 0
    for term in document_term_matrix:
      dot_product += document_term_matrix[term] * query_vector[term]
    
    # Calculate the Euclidian to normalize the document and query vectors
    magnitude_query = sum([value**2 for value in query_vector.values()])
    magnitude_document = sum([value**2 for value in document_term_matrix.values()])

    # calculate the cosine similarity
    if (magnitude_query * magnitude_document) == 0:
      similarity = 0
    else:
      similarity = dot_product / ((magnitude_query * magnitude_document) ** 0.5)
    return similarity
  
  # Relevant Judgement
  # https://www.futurelearn.com/courses/mechanics-of-search/4/steps/1866826
  def query(self, query):
    similarity = self.calculate_similarity(query)
    # delete the similarity scores = 0
    relevance_judgement_rank = []
    for docno, score in similarity.items():
      # if score > 0:
        relevance_judgement_rank.append({ docno: score })
    # sort the similarity scores (descending)
    relevance_judgement_rank.sort(key=lambda x: list(x.values())[0], reverse=True)
    # print(relevance_judgement_rank)
    return relevance_judgement_rank


if __name__ == "__main__":
  print("===================================================")
  print("Search Engine - Vector Space Model - Query sized Vector")
  print("===================================================")
  print("Author: Emerson Takeshi Urushibata")


  parser=argparse.ArgumentParser(description="sample argument parser")
  parser.add_argument("keywords", help="Search Keywords")
  args=parser.parse_args()

  # for testing purpose, define the collection size
  # limit = 3 # any number or None
  limit = None
  collection = CorpusIndexer('./dataset/manifest.xml', limit)
  ranking_vsm = RankingVSM_Q(collection)

  similarity = ranking_vsm.query(args.keywords)
  print(f"Searching for {args.keywords}")
  print("===================================================")
  print("Results:")
  print(similarity)