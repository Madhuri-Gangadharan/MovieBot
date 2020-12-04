import joblib
import pandas as pd
import os,sys
sys.path.append(os.path.normpath(os.getcwd()))

from nlp.nlp_solutions.nlplearn import metadata_filtering, tfidf_fit
from config import onetime_file

if __name__ == "__main__":
    
    metadata = pd.read_csv('data/metadata_prep.csv')

    documents = metadata['overview'].fillna('')
    cosine_sim = metadata_filtering(documents)
    indices = pd.Series(metadata.index, index=metadata['title']).drop_duplicates()
    
    documents = list(metadata['title'].fillna(''))
    tfidf_fit, tfidf_matrix = tfidf_fit(documents)

    i = [cosine_sim,indices,tfidf_fit, tfidf_matrix]
    joblib.dump(i,onetime_file)
