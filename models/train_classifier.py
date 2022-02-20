import sys
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import string
import sqlite3
import pickle
from sklearn.feature_extraction.text import CountVectorizer

def load_data(database_filepath):
    conn = sqlite3.connect(database_filepath)
    df = pd.read_sql('SELECT * FROM disaster_message', conn)
    return (df)


def tokenize(text):
    punc_numbers = string.punctuation + '0123456789'
    text = ''.join([l for l in text if l not in punc_numbers])
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)
    
    return (" ".join(str(token) for token in clean_tokens))


def build_model():
    database_filepath = './data/disaster_messages_data.db'
    load_data(database_filepath)
    df['tokens'] = df['messages'].apply(tokenize)
    vect = CountVectorizer(min_df= .01)

    X = vect.fit_transform(df['tokens'])

    y = df[['related', 'request', 'offer', 'aid_related',
       'medical_help', 'medical_products', 'search_and_rescue', 'security',
       'military', 'child_alone', 'water', 'food', 'shelter', 'clothing',
       'money', 'missing_people', 'refugees', 'death', 'other_aid',
       'infrastructure_related', 'transport', 'buildings', 'electricity',
       'tools', 'hospitals', 'shops', 'aid_centers', 'other_infrastructure',
       'weather_related', 'floods', 'storm', 'fire', 'earthquake', 'cold',
       'other_weather']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 21)
    model = MultiOutputClassifier(KNeighborsClassifier()).fit(X_train, y_train)
    
    return model


def evaluate_model(model, X_test, Y_test, category_names):

    pass


def save_model(model, model_filepath):
    filename = './models/classifier.pkl'
    pickle.dump(model, open(filename, 'wb'))
    pickle.dump(model, open(filename, 'wb'))
    pass


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()