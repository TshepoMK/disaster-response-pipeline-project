# disaster-response-pipeline-project
Udacity nano degree submission




![word cloud](https://user-images.githubusercontent.com/12718924/154844685-9cfdfc67-4b97-48a2-b18d-1b87bdeb72c5.png)


This Project is part of Data Science Nanodegree Program by Udacity in collaboration with Figure Eight. The initial dataset contains pre-labelled tweet and messages from real-life disaster. The aim of the project is to build a Natural Language Processing tool that categorize messages.

This project is for Udacity Nano Degree submission. The objective of this project is to build 3 pipelines. 

### 1. The first pipeline is a data processing pipeline
* This pipeline reads in 2 CSV files of disaster tweets and the category in which the tweets falls under, there are 36 Categories. 
* The second function the of the pipeline is to merger the two files.
* The third function is to clean the data and to save the resulting dataframe into a sqlite database.
* The code for all of the steps above can be found on the process_data.py file in the data folder.

### 2. Second pipeline is a Machine Learning Pipeline

* This pipeline reads in the database data (disaster_response_messages.db)
* Then it tokenizes the messages, creating clean token that have been normalized, and then vectorizes the text to create numerical inputs.
* And the trains a multioutput Machine Learning model and then pickles the model classifier.pkl and then saves it. The code can be found on the train_classifier.py file

### To run the project

clone the repository ``
and then on your terminal navigate to the folder app.
and the run the following command `python run.py` the follwing output will be displayed

![flask app](https://user-images.githubusercontent.com/12718924/154844680-e37066b8-2c83-4a81-9eb0-ab3f77bd3bba.png)
and then on your web browser go to http:127.0.0.1:3001

This is the landing page you should see

![landing page](https://user-images.githubusercontent.com/12718924/154844682-82042f84-ba0a-4d59-a0f7-b1b0932f5e6b.png)


