import sys
import sqlite3
import pandas as pd


def load_data(messages_filepath, categories_filepath):
    """
    This function loads the data from the csv files and merges them into a single dataframe.
    
    """
    messages_filepath = './data/disaster_categories.csv'
    categories_filepath = './data/disaster_categories.csv'

    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)

    merged_data = pd.merge(messages, categories, on='id')

    return (merged_data)



def clean_data(merged_data):
    """
    This function cleans the data by removing the duplicates and dropping the columns that are not needed.
    """

    categories_df = merged_data['categories'].str.split(';', expand=True)

    column_names = list(categories_df.iloc[0])
    new_column_names = []

    for names in column_names:
        new_column_names.append(names.split('-')[0])
    
    categories_df = categories_df.set_axis(new_column_names, axis=1)


    for name in new_column_names:
        categories_df[name] = categories_df[name].str.replace(name + '-',' ')
    
    categories_df['id'] = merged_data['id']


    disaster_training_data = pd.merge(merged_data, categories_df, on='id')

    disaster_training_data.drop('original',axis=1)
    disaster_training_data.index = disaster_training_data['id']
    disaster_training_data.drop(['id','original'], axis=1, inplace=True)

    return disaster_training_data
 


def save_data(disaster_training_data, database_filename):
    """
    This function saves the cleaned data into a database.
    
    """

    conn = sqlite3.connect('disaster_messages_data.db')

    # get a cursor
    cur = conn.cursor()


    # drop the test table in case it already exists
    cur.execute("DROP TABLE IF EXISTS disaster_message")
    
        # create the table with text id as a primary key
    cur.execute("CREATE TABLE disaster_message (id INTERGER, message TEXT, genre TEXT, related INTEGER, request INTEGER,\
    offer INTEGER, aid_related INTEGER, medical_help INTEGER, medical_products INTEGER,search_and_rescue INTEGER,\
    security INTEGER, military INTEGER, child_alone INTEGER, water INTEGER, food INTEGER, shelter INTEGER,\
    clothing INTEGER, money INTEGER, missing_people INTEGER, refugees INTEGER, death INTEGER, \
    other_aid INTEGER, infrastructure_related INTEGER, transport INTEGER, buildings INTEGER, \
    electricity INTEGER, tools INTEGER, hospitals INTEGER, shops INTEGER, aid_centers INTEGER,\
    other_infrastructure INTEGER, weather_related INTEGER, floods INTEGER, storm INTEGER, \
    fire INTEGER, earthquake INTEGER,cold INTEGER, other_weather INTEGER, direct_report INTEGER);")

    # insert the data into the table
    disaster_training_data.to_sql(name='disaster_message', con=conn, if_exists='replace', index=True)

    # commit the changes

    conn.commit()
    conn.close()

    pass


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()