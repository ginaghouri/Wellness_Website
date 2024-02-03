
from unittest import TestCase, main
from unittest.mock import MagicMock
from bson import ObjectId
from bson.json_util import dumps
from random import uniform
from flask import Flask
import pandas as pd

from utils import sentiment_analysis
from models import JournalEntry, MongoDBConn, Journal
from config import client, journal


class TestMongoDBConn(TestCase):
    """
    Testing MongoDB connection via Journal.
    """

    def setUp(self):
        """
        Setting up resources needed for test cases, connects to the db.
        """

        # override setUp from unittest.
        self.journal = journal


    def test_str(self):
        """
        Tests the connection to the chillpill DB.
        """

        self.assertIn('chillpill', str(self.journal.dbconn))


class TestJournalEntry(TestCase):
    """
    Test JournalEntry.
    """

    def test(self):
        """
        Tests an instance of an entry, checks for matching details.
        """

        # add a new journal entry to test
        body = 'Test body'
        sentiment = float(f'{uniform(0, 10):.2f}')
        
        # testing the entry object.
        entry = JournalEntry(body, sentiment)

        self.assertEqual(entry.body, body)
        self.assertEqual(entry.sentiment, sentiment)


class TestJournalManager(TestCase):
    """
    Test JournalManager via Journal.
    """

    def setUp(self):
        """
        Setting up resources needed for test cases, connects to the db.
        """

        # use a test db.
        db = client['testdb']

        # setup flask server.
        app = Flask(__name__)
        app.config['MONGO_URI'] = 'mongodb://localhost:27017/testdb'

        # send the app to the MongoDB and Journal.
        mongo_conn = MongoDBConn(app)
        self.journal = Journal(mongo_conn)

        # delete all entries in collection, refreshing.
        self.journal.dbconn.db.log.delete_many({})
        

    def test_create(self):
        """
        Tests the create method by simulating an entry and checking the details match.
        """

        body = 'Test body'
        sentiment = float(f'{uniform(0, 10):.2f}')

        _id = self.journal.manager.create(body, sentiment)

        # look for the entry.
        inserted = self.journal.manager.read_one(_id)[0]
        
        # check the details match.
        self.assertIsNotNone(inserted['_id']['$oid'])
        self.assertEqual(inserted['body'], body)
        self.assertEqual(inserted['sentiment'], sentiment)
        

    def test_read_all(self):
        """
        Tests all entries in the db match the entries read by the journal manager.
        """
        
        # find all entries in the db log collection.
        db_entries = dumps(self.journal.dbconn.db.log.find())

        # find the entries the Journal class returns.
        class_entries = dumps(self.journal.manager.read_all())

        self.assertEqual(db_entries, class_entries)


    def test_read_one(self):
        """
        Tests the return of read_one() returns 1 entry.
        """

        # setup and create an entry.
        body = 'Test single body'
        sentiment = float(f'{uniform(0, 10):.2f}')

        _id = self.journal.manager.create(body, sentiment)

        # read an entry from the journal.
        check = self.journal.manager.read_one(_id)

        # check the return length is 1.
        self.assertEqual(len(check), 1)
    

    def test_check_one(self):
        """
        Tests a query exists in the DB.
        """
        
        # setup and create an entry.
        body = 'Test body'
        sentiment = float(f'{uniform(0, 10):.2f}')

        self.journal.manager.create(body, sentiment)
        
        query = {
            'body': 'New body',
            'sentiment': float(f'{uniform(0, 10):.2f}')
        }

        # query should return False, not in DB.
        self.assertFalse(self.journal.manager.check_one(query))


    def test_update(self):
        """
        Tests update functionality.
        """
        
        # create a test entry.
        test_entry_id = self.journal.manager.create("initial_body", sentiment_analysis("initial_body"))

        # updated data.
        update_data = {
            "body": "slayy",
            'sentiment': sentiment_analysis('slayy')
        }

        # update and retrieve the entry.
        self.journal.manager.update(test_entry_id, update_data)
        updated_entry = self.journal.dbconn.db.log.find_one({"_id": ObjectId(test_entry_id)})

        self.assertEqual(updated_entry['body'], update_data['body'])
        self.assertEqual(updated_entry['sentiment'], update_data['sentiment'])
    

    def test_delete(self):
        """
        Tests delete functionality.
        """

        # create and delete an entry.
        test_entry_id = self.journal.manager.create("I'm trying", sentiment_analysis("I'm trying"))
        self.journal.manager.delete(test_entry_id)

        # check the entry is none.
        deleted_entry = self.journal.dbconn.db.log.find_one({"_id": ObjectId(test_entry_id)})
        self.assertIsNone(deleted_entry, "we did it saima")


class TestMoodTracker(TestCase):
    """
    Test MoodTracker via Journal.
    """

    def setUp(self):
        """
        Setting up resources needed for test cases, connects to the db.
        """

        # use a test db
        db = client['testdb']

        # setup flask server.
        app = Flask(__name__)
        app.config['MONGO_URI'] = 'mongodb://localhost:27017/testdb'

        # send the app to the MongoDB and Journal.
        mongo_conn = MongoDBConn(app)

        # override the collection in MongoDBConn for distinct entries.
        mongo_conn.collection = mongo_conn.db.testing
        self.journal = Journal(mongo_conn)

        # delete all entries in collection, refreshing.
        self.journal.dbconn.db.testing.delete_many({})

        # override data in recent_data method for plotting.
        self.data = [
            {'timestamp': '2023-11-30',
             'sentiment': 5.21},
            {'timestamp': '2023-12-01',
             'sentiment': 8.37}
             ]
        # mock the return of the recent_data() method.
        self.mock_data = MagicMock(return_value=pd.DataFrame(self.data))

        # create test entries.
        self.entries = [
            {'body': 'Feeling super sad today, because the ice cream shop ran out of my favourite flavour.'},
            {'body': "Had the very best time today in my CFG session, we learnt search and sort algorithms which I'm sure will come in super handy."},
            {'body': 'Ice cream store is back with my flavour, yay!!! SO happy! :)'},
            {'body': 'Customers are so annoying, especially in the early mornings. I HATE my job!.'},
            {'body': "You know what? My job isn't so bad. I get to interact with so many different people and having a job is a blessing."}
            ]

        # send to testing collection.
        self.create_entries(self.entries)
    

    def test_plot_mood(self):
        """
        Tests the plotting functionality.
        """

        # override the return of the recent_data() method
        self.journal.mood.recent_data = self.mock_data
        plot = self.journal.mood.plot_mood()

        # ensure data has been plotted.
        for i in self.data:
            self.assertIn(str(i['timestamp']), plot)
            self.assertIn(str(i['sentiment']), plot)

        # ensure random data has not been plotted.
        self.assertNotIn('2023-11-31', plot)
        self.assertNotIn('3.98', plot)
    

    def create_entries(self, entries):
        """
        Sends the entries to the testing collection.
        """
        
        for entry in entries:
            body = entry['body']
            sentiment = sentiment_analysis(body)
            self.journal.manager.create(body, sentiment)


    def test_min_sentiments(self):
        """
        Tests correctly reads 3 lowest sentiment values.
        """

        self.assertIn('2.43', self.journal.mood.min_sentiments())
        self.assertIn('2.50', self.journal.mood.min_sentiments())
        self.assertIn('3.98', self.journal.mood.min_sentiments())


    def test_max_sentiments(self):
        """
        Tests correctly reads 3 highest sentiment values.
        """

        self.assertIn('7.15', self.journal.mood.max_sentiments())
        self.assertIn('6.55', self.journal.mood.max_sentiments())
        self.assertIn('3.98', self.journal.mood.max_sentiments())


    def test_av_sentiments(self):
        """
        Tests correctly reads average of last 7 sentiment values.
        """

        # only 5 entries being tested.
        manual_av = (3.98 + 6.55 + 7.15 + 2.43 + 2.50) / 5

        # test that calculated average is the same as the returned.
        self.assertIn(str(format(manual_av, '.2f')), self.journal.mood.av_sentiment())


if __name__ == '__main__':
    main()
