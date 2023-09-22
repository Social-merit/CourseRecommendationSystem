from os import read

from flask import Flask, request, render_template

import pandas as pd
import numpy as np
import neattext.functions as nfx
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from dashboard import getvaluecounts, getlevelcount, getsubjectsperlevel, yearwiseprofit


# Initialize Flask app
app = Flask(__name__)


# Define a function to create a matrix of Count Vectorized course titles
def getcosinemat(df):
    countvect = CountVectorizer()
    cvmat = countvect.fit_transform(df['Clean_title'])
    return cvmat


# getting the title which doesn't contain stopwords and all which we removed with the help of nfx
# Function to clean the course titles by removing stopwords, special characters, etc.
def getcleantitle(df):
    df['Clean_title'] = df['course_title'].apply(nfx.remove_stopwords)
    df['Clean_title'] = df['Clean_title'].apply(nfx.remove_special_characters)

    return df

# Compute the Cosine Similarity matrix from Count Vectorized matrix
def cosinesimmat(cv_mat):
    return cosine_similarity(cv_mat)

# Read data from a CSV file
def readdata():

    df = pd.read_csv('UdemyCleanedTitle.csv')
    return df

#Main recommendation logic for a particular title which is choosen
# Main function for recommending courses based on Cosine Similarity
def recommend_course(df, title, cosine_mat, numrec):
    course_index = pd.Series(
        df.index, index=df['course_title']).drop_duplicates()
    index = course_index[title]
    scores = list(enumerate(cosine_mat[index]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    selected_course_index = [i[0] for i in sorted_scores[1:]]

    selected_course_score = [i[1] for i in sorted_scores[1:]]

    rec_df = df.iloc[selected_course_index]

    rec_df['Similarity_Score'] = selected_course_score

    final_recommended_courses = rec_df[[
        'course_title', 'Similarity_Score', 'url', 'price', 'num_subscribers']]

    return final_recommended_courses.head(numrec)

# this will be called when a part of the title is used,not the complete title!

# Search for courses by term
def searchterm(term, df):
    result_df = df[df['course_title'].str.contains(term)]
    top6 = result_df.sort_values(by='num_subscribers', ascending=False).head(6)
    return top6


# Extract some features like URL, title, and price from dataframe
def extractfeatures(recdf):

    course_url = list(recdf['url'])
    course_title = list(recdf['course_title'])
    course_price = list(recdf['price'])

    return course_url, course_title, course_price

 # Define the home route of the web application
# Define the main route of the web application, which supports both GET and POST methods
@app.route('/', methods=['GET', 'POST'])
def hello_world():

    # Check if the request method is POST
    if request.method == 'POST':

        # Collect form data from the client
        my_dict = request.form
        titlename = my_dict['course']

        # Read the data from the CSV file
        df = readdata()

        try:
            # Clean the course titles in the DataFrame
            df = getcleantitle(df)

            # Get the Count Vectorized matrix for course titles
            cvmat = getcosinemat(df)

            # Set the number of recommendations to show
            num_rec = 6

            # Calculate the cosine similarity matrix from the Count Vectorized matrix
            cosine_mat = cosinesimmat(cvmat)

            # Get the recommended DataFrame based on the chosen title and other parameters
            recdf = recommend_course(df, titlename, cosine_mat, num_rec)
            
        except:
            # Search for courses that contain the term if any exception occurs
            recdf = searchterm(titlename, df)

            # Limit to top 6 if more than 6 results
            if recdf.shape[0] > 6:
                recdf = recdf.head(6)

        # Extract features like URL, title, and price from the recommended DataFrame
        course_url, course_title, course_price = extractfeatures(recdf)

        # Create a mapping between course titles and their URLs
        coursemap = dict(zip(course_title, course_url))

        # Check if any courses were found and render the appropriate template
        if len(coursemap) != 0:
            return render_template('index.html', coursemap=coursemap, coursename=titlename, showtitle=True)
        else:
            return render_template('index.html', showerror=True, coursename=titlename)

    # If the request method is GET, just render the default index.html
    return render_template('index.html')


# Define the dashboard route of the web application
# Define the dashboard route of the web application, supporting both GET and POST methods
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    # Read the data from a CSV file into a DataFrame
    df = readdata()

    # Get the count of unique values for some specific column(s) from the DataFrame
    valuecounts = getvaluecounts(df)

    # Get counts of different course levels (like Beginner, Intermediate, etc.)
    levelcounts = getlevelcount(df)

    # Get counts of subjects per each level
    subjectsperlevel = getsubjectsperlevel(df)

    # Get various metrics related to profit and subscribers, possibly aggregated by year or month
    yearwiseprofitmap, subscriberscountmap, profitmonthwise, monthwisesub = yearwiseprofit(df)

    # Render the dashboard.html template and pass all the calculated data for display
    return render_template('dashboard.html', valuecounts=valuecounts, levelcounts=levelcounts,
                           subjectsperlevel=subjectsperlevel, yearwiseprofitmap=yearwiseprofitmap, 
                           subscriberscountmap=subscriberscountmap, profitmonthwise=profitmonthwise, 
                           monthwisesub=monthwisesub)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
