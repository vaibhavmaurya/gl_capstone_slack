__all__ = ['preprocess', 'preprocess_predict']

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
import os
import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import string
import re
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from sklearn.preprocessing import StandardScaler
import pandas as pd


nltk.download('stopwords',quiet=True) # stopword library
nltk.download('wordnet', quiet=True) # wordnet library
nltk.download('words', quiet=True) # words library
nltk.download('punkt', quiet=True) # tokenize library
nltk.download('omw-1.4', quiet=True)


# remove punctuations
translate_table = dict((ord(char), None) for char in string.punctuation) 
stop_words = stopwords.words('english')

# Lemmatization instance
lemmatizer = WordNetLemmatizer()

# Use stemmer
ps = PorterStemmer()

def clean_text(text):
  text = text.lower()
  #Remove punctuation
  text = text.translate(translate_table)
  # Remove alphanumerics
  text = re.sub('[^a-zA-Z]',' ', str(text))

  words = word_tokenize(text)
  filtered_words = [ps.stem(lemmatizer.lemmatize(word)) for word in words if word not in stop_words and len(word) > 2]
  return " ".join(filtered_words)

  


def preprocess(df:pd.DataFrame, col_config:dict) -> None:

    categorical_columns = col_config['categorical_columns']
    text_column = col_config['description_column']

    preprocess_path = os.getenv('PREPROCESS_PATH')
    if not os.path.exists(preprocess_path):
        raise Exception(f'''Preprocessing.preprocess(): Save preprocess obj path is not valid
                        path: {preprocess_path}
                    ''')

    preprocess_path = os.path.join(preprocess_path,'preprocess.pkl')

    # One hot encoder
    one_hot_encoder = OneHotEncoder(drop='first')

    # tfidf encoder
    tfidf_encoder = TfidfVectorizer(max_features=500,
                      preprocessor=clean_text,
                      analyzer='word',
                      # stop_words = 'english',
                      lowercase=True,
                      use_idf=True)

    # Column Transformer
    column_trans = ColumnTransformer(
        [('categories', one_hot_encoder, categorical_columns), \
        ('text', tfidf_encoder, text_column)
        ],
        remainder='passthrough',
        verbose_feature_names_out=False)


    column_trans.fit(df[categorical_columns+[text_column]])

    # save the preprocess
    with open(preprocess_path, 'wb') as f:
        pickle.dump(column_trans, f)
    
    return column_trans.transform(df[categorical_columns+[text_column]]).toarray()




def preprocess_predict(df: pd.DataFrame, col_config:dict):

    # load the preprocess object
    preprocess_path = os.getenv('PREPROCESS_PATH')
    if not os.path.exists(preprocess_path):
        raise Exception(f'''Preprocessing.preprocess(): Save preprocess obj path is not valid
                        path: {preprocess_path}
                    ''')
    preprocess_path = os.path.join(preprocess_path,'preprocess.pkl')
    with open(preprocess_path, 'rb') as f:
        column_trans = pickle.load(f)

    # Get all the relevent columns
    categorical_columns = col_config['categorical_columns']
    text_column = col_config['description_column']

    # Check if columns are aligned properly
    try:
        # print(df.columns)

        # print(categorical_columns+[text_column])
        df = df[categorical_columns+[text_column]]
    except Exception as e:
        print(f'''Preprocessing.preprocess_predict():
        Error reason:
        {e}
        ''')
        raise Exception(f'''Preprocessing.preprocess_predict():
            It seems the the data fields does not match with the
            fields mentioned in the configuration
        ''')

    return column_trans.transform(df).toarray()

    
    