#!/usr/bin/python
from stopwords import escape_sequence, remove_stopwords, get_punctuation
import xmltodict
import json
import string

class CorpusIndexer:
  # limit_documents is used to limit the number of documents to be processed for development purposes
  def __init__(self, file_path, limit_documents=None):
    self.documents = []
    with open(file_path, 'r') as f:
      data = f.read()

    # Wrap the data in a root tag since it isn't a XML data structure without a root element
    data = f"<root>{data}</root>"

    # Parse the XML data
    xml_dict = xmltodict.parse(data)
    json_data = json.dumps(xml_dict, indent=2)
    # Parse the JSON data
    self.documents = json.loads(json_data)['root']['doc']

    if (limit_documents is not None):
      self.documents = self.documents[:limit_documents]

    print(f'Total documents loaded: {len(self.documents)}')

    self.generate_tokens()

  def get_documents(self):
    return self.documents

  def get_document(self, docno):
    for doc in self.documents:
      if int(doc['docno']) == int(docno):
        return doc
    return None
  
  def tokenize_document(self, docno):
    for doc in self.documents:
      if int(doc['docno']) == int(docno):
        text = doc['text']

        # return empty tokens if text is None or ""
        if (text is None):
          return []

        # remove punctuation from document
        text.translate(str.maketrans('', '', get_punctuation()))

        # Remove dots and commas following the rule that comma has a space after it and dot has a space before it
        text = text.replace(", ", " ").replace(" .", " ")

        # Remove escape sequences
        for escape in escape_sequence():
          text = text.replace(escape, " ")

        # Tokenize the text by splitting by spaces
        tokens = text.lower().split()
        return tokens
        
  # Process of cleaning the tokens: Stopwords removal, stemming, etc.
  def clean_tokens(self, tokens):
    tokens_lower = [token.lower() for token in tokens]
    tokensWOStopWords = remove_stopwords(tokens_lower)
    # remove duplicate
    # remove_duplicate_tokens = list(set(tokensWOStopWords))
    # return remove_duplicate_tokens
    return tokensWOStopWords
  
  def clean_tokens_by_document(self, docno):
    tokens = self.tokenize_document(docno)
    return self.clean_tokens(tokens)

  def generate_tokens(self):
    for doc in self.documents:
      doc['clean_tokens'] = self.clean_tokens_by_document(doc['docno'])

  #  create a terms index of the collection in format: {term: [docno1, docno1, docno2, ...]}
  #  terms that appear more than once is repeated in the list
  def generate_terms_index(self):
    terms_index = {}
    for doc in self.documents:
      for token in doc['clean_tokens']:
        if token in terms_index:
          terms_index[token].append(doc['docno'])
        else:
          terms_index[token] = [doc['docno']]
    return terms_index
    
  # Term-Document Matrix - Freqency Model
  # https://www.futurelearn.com/courses/mechanics-of-search/4/steps/1866810
  # create a term-document matrix by frequency model in format: {term1: {docno1: 0, docno2: 2}, term2: {docno1: 1, docno2: 0}}
  # where 1+ means the term is present in the document and 0 otherwise.
  def generate_term_document_matrix(self):
    terms_index = self.generate_terms_index()
    # print(terms_index)
    term_document_matrix = {}
    for term in terms_index:
      term_document_matrix[term] = {}
      for doc in self.documents:
        term_document_matrix[term][int(doc['docno'])] = doc['clean_tokens'].count(term)
    # print(term_document_matrix)
    return term_document_matrix


  # Document-Term Matrix - Freqency Model
  # https://www.futurelearn.com/courses/mechanics-of-search/4/steps/1866813
  # create a DOCUMENT-TERM matrix by frequency model in format: {docno1: {term1: 0, term2: 2}, docno2: {term1: 1, term2: 0}}
  # where 1+ means the term is present in the document and 0 otherwise.
  def generate_document_term_matrix(self):
    term_document_matrix = self.generate_term_document_matrix()
    document_term_matrix = {}
    for term in term_document_matrix:
      for docno, count in term_document_matrix[term].items():
        if docno in document_term_matrix:
          document_term_matrix[docno][term] = count
        else:
          document_term_matrix[docno] = {term: count}
    # print(document_term_matrix)
    return document_term_matrix