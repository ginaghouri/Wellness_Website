
from flask_pymongo import PyMongo
from datetime import datetime as dt
from bson import json_util, ObjectId
import json
from plotly.offline import plot
import plotly.express as px
import pandas as pd
from markupsafe import Markup
import numpy as np
from abc import ABC, abstractmethod


class DBConn:
    """
    Connect to a database.
    """

    @abstractmethod
    def get_collection(self):
        """
        Connects to a collection in a DB.
        """


class DataManager(ABC):
    """
    CRUD functionalities for a database.
    """

    @abstractmethod
    def create(self, *args):
        """
        Creates a record.
        """

    @abstractmethod
    def read_all(self):
        """
        Reads all records.
        """
    
    @abstractmethod
    def read_one(self, *args):
        """
        Reads one record.
        """

    @abstractmethod
    def update(self, *args, **kwargs):
        """
        Updates a record.
        """

    @abstractmethod
    def delete(self, *args):
        """
        Deletes a record.
        """


class MongoDBConn(DBConn):
    """
    Inherits from DBConn to connect to our MongoDB.
    """

    def __init__(self, app):
        self.mongo = PyMongo(app)
        self.db = self.mongo.db
        self.collection = self.mongo.db.log
    

    def __str__(self):
        """
        Checks the MongoDB collection.
        """

        # connection check.
        return f'MongoDB Connection: {self.db.name}'
    

    def get_collection(self):
        """
        Returns a collection from a MongoDB.
        """
        return self.collection


class JournalEntry:

  def __init__(self, body, sentiment):
    """
    An instance of a journal entry.
    """
    
    self.body = body
    self.sentiment = sentiment
    self.timestamp = dt.now().strftime("%d/%m/%Y %H:%M:%S")


class JournalManager(DataManager):
    """
    Inherits from DataManager for the journal CRUD functionalities.
    """

    def __init__(self, dbconnection):

        # get the collection from the DB connection.
        self.collection = dbconnection.get_collection()
    

    def create(self, body, sentiment):
        """
        Creates a journal entry and sends it to the collection.
        """

        # initialise a journal entry as an object.
        entry = JournalEntry(body, sentiment)

        # add entry to mongo db collection.
        submission = self.collection.insert_one({
        'body': entry.body,
        'sentiment': entry.sentiment,
        'timestamp': entry.timestamp
        })
    
        # return entry id
        return submission.inserted_id


    def read_all(self):
        """
        Returns all entries in the log collection.
        """
        
        # return all entries.
        all_entries = self.collection.find()

        # returns in json formatting.
        return json.loads(json_util.dumps(all_entries))
    
   
    def read_one(self, _id):
        """
        Reads a single entry based on its id.
        """
        
        # return a single entry.
        entry = self.collection.find({'_id': ObjectId(_id)})

        return json.loads(json_util.dumps(entry))
    

    def check_one(self, query):
        """
        Checks that an entry exists based on a query.
        """

        # check that a query exists.
        if self.collection.find_one(query):
            return True
        return False
    
    
    def update(self, _id, update_data):
        """
        Updates an entry with new data based on its id.
        """
        
        self.collection.update_one(
            {"_id": ObjectId(_id)},
            {"$set": update_data}
            )

    
    def delete(self, _id):
        """
        Deletes an entry with an _id.
        """
        
        self.collection.delete_one(
            {"_id": ObjectId(_id)}
            )
 

class MoodTracker:
    """
    Mood tracker functionality.
    """
    
    def __init__(self, dbconnection):
        self.collection = dbconnection.get_collection()
        
    
    def recent_data(self):
        """
        Fetches the most recent data from the DB.
        """

        # return updated data.
        return pd.DataFrame(list(self.collection.find(
            {},
            {'sentiment': 1, 'timestamp': 1}
            )))
    
    
    def plot_mood(self):
        """
        Plots a graph of the sentiment values against datetime.
        """

        df = self.recent_data().copy()

        # clean up None values.
        df['sentiment'].replace({None: pd.NA}, inplace=True)
        df.dropna(subset=['sentiment'], inplace=True)

        try:
            # convert 'sentiment' column to numeric.
            df['sentiment'] = pd.to_numeric(df['sentiment'])
        
        except KeyError:
            # if 'sentiment' column doesn't exist, manually get the data.
            sentiment = [entry['sentiment'] for entry in list(self.collection.find({}, {'sentiment': 1}))]

            try:
                # converting to numeric again.
                df['sentiment'] = pd.to_numeric(sentiment, errors='raise')
            
            except TypeError as e:
                print("Please see error below.")
                print(e)

                # final try, set the column to empty.
                df['sentiment'] = []

        # setup plot.
        fig = px.line(df, x='timestamp', y='sentiment', title='Your Mood So Far!')

        # add plot markers.
        fig.update_traces(mode='lines+markers')
        
        colors = np.where(df['sentiment'] < 4, '#add8e6', np.where(df['sentiment'] <= 6, '#c5a3ff', '#ffb6c1'))
        
        # plot styling.
        fig.update_traces(marker=dict(color=colors), line=dict(color='#c36c83'))
        fig.update_layout(
            plot_bgcolor='#f7c7d8',
            paper_bgcolor='white',
            font=dict(color='#c36c83'),
            title=dict(font=dict(color='#f0668c')),
            yaxis=dict(
                range=[0, 10],
                linecolor='white',
                linewidth=2
            ),
            xaxis=dict(
                linecolor='white',
                linewidth=2
            ),
            margin=dict(l=40, r=40, t=40, b=40)
        )
        my_plot = plot(fig, output_type='div', include_plotlyjs=True)

        # markup the figure as HTML
        return Markup(my_plot)
    

    def min_sentiments(self):
        """
        Retrieve data of 3 lowest sentiment entries.
        """

        # sort sentiment values by ascending.
        lowest_posts = self.collection.find({'sentiment': {'$ne': None}}).sort('sentiment', 1).limit(3)
        
        # setup result string with sentiment and timestamp to return.
        result_string = "Your lowest moments were:<br>"
        for index, post in enumerate(lowest_posts, 1):
            sentiment = post['sentiment']
            timestamp = post['timestamp']
            result_string += f"{index}. Timestamp: {timestamp}, <br>Sentiment: {sentiment}<br>"

        return Markup(result_string)


    def max_sentiments(self):
        """
        Retrieve data of 3 highest sentiment entries.
        """

        # sort sentiment values by descending.
        highest_posts = self.collection.find({'sentiment': {'$ne': None}}).sort('sentiment', -1).limit(3)
        
        # setup result string with sentiment and timestamp to return.
        result_string = "Your highest moments were:<br>"
        for index, post in enumerate(highest_posts, 1):
            sentiment = post['sentiment']
            timestamp = post['timestamp']
            result_string += f"{index}. Timestamp: {timestamp}, <br>Sentiment: {sentiment}<br>"

        return Markup(result_string)
  
 
    def av_sentiment(self):
        """
        Retrieve average sentiment data from the last seven posts.
        """

        # find the most recent seven posts, ordering by timestamp.
        entries = self.collection.find({'sentiment': {'$ne': None}}).sort('timestamp', -1).limit(7)

        try:
            # extra caution to remove None values.
            sentiment_scores = pd.to_numeric([float(entry['sentiment']) for entry in entries], errors='raise')
        
        except TypeError as e:
            print("Please see error below.")
            print(e)
            return "No valid sentiment scores to display"
        
        else:
            # return average sentiment if exists.
            if len(sentiment_scores) > 0:
                average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
                return f"The average sentiment of your last 7 entries is: {average_sentiment:.2f}"
                
            else:
                return "No valid sentiment scores to display"


class Journal:
    """
    Connecting the entire journal to the MongoDB.
    """
    
    def __init__(self, dbconn):
        # get the connection and send to our journal manager and mood tracker.
        self.dbconn = dbconn
        self.manager = JournalManager(self.dbconn)
        self.mood = MoodTracker(self.dbconn)
