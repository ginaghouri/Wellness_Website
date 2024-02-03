
from unittest import TestCase, main
from unittest.mock import patch
from random import uniform
from utils import sentiment_analysis, daily_affirmation


class TestSentiment(TestCase):
    """
    Tests sentiment analysis.
    """

    def test_sentiment(self):
        """
        Tests correct sentiment returns.
        """

        # objective texts.
        self.assertIsNone(sentiment_analysis('I am a frog.'), 'Objective texts should return None.')

        # subjective texts should return a sentiment.
        self.assertIsNotNone(sentiment_analysis('I had a great day today!'), 'Highly subjective texts should not return None.')

        # sentiment should return a string.
        self.assertIsInstance(sentiment_analysis('I had a great day today!'), str, 'Sentiment should be returned as a string.')


class TestAffirmation(TestCase):
    """
    Tests daily affirmations return.
    """

    @patch('utils.random.choice', side_effect=lambda x: x[0])
    def test_neg(self, choice):
        """
        Tests negative sentiments, returning the first item in the arrays. `choice` arg represents patched random.choice parameter.
        """

        # test vneg: 0 < sentiment <= 2.
        sentiment = format(uniform(0, 2), '.2f')
        self.assertEqual(daily_affirmation(float(sentiment)), 'Get yourself a Maccies today.')

        # test neg: 2 < sentiment <= 4.
        sentiment = format(uniform(2.01, 4), '.2f')
        self.assertEqual(daily_affirmation(float(sentiment)), "People don't slay everyday, and today is not your slay day. Make tomorrow your slay day.")


    @patch('utils.random.choice', side_effect=lambda x: x[1])
    def test_neutral(self, choice):
        """
        Tests neutral sentiments, returning the second item in the array. `choice` arg represents patched random.choice parameter.
        """

        # test neutral: 4 < sentiment <= 6.
        sentiment = format(uniform(4.01, 6), '.2f')
        self.assertEqual(daily_affirmation(float(sentiment)), 'Go get yourself a cuppa and a biscuit, you need it!')
    

    @patch('utils.random.choice', side_effect=lambda x: x[0])
    def test_pos(self, choice):
        """
        Tests positive sentiments, returning the second item in the array. `choice` arg represents patched random.choice parameter.
        """

        # test pos: 6 < sentiment <= 8.
        sentiment = format(uniform(6.01, 8), '.2f')
        self.assertEqual(daily_affirmation(float(sentiment)), 'Even your hair is great today!')

        # test vpos: 8 < sentiment <= 10.
        sentiment = format(uniform(8.01, 10), '.2f')
        self.assertEqual(daily_affirmation(float(sentiment)), "Keep doing what you're doing!")
    

    def test_not_in_range(self):
        """
        Tests out of range sentiments.
        """
        sentiment = format(uniform(10.01, 12), '.2f')
        self.assertEqual(daily_affirmation(float(sentiment)), 'Something has gone wrong.')


if __name__ == '__main__':
    main()
