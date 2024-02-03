import requests
from textblob import TextBlob
import random


def sentiment_analysis(text):
    """
    Sentiment analysis of a piece of text. Returns the positivity value on a scale of 0 - 10.
    """

    url = 'http://text-processing.com/api/sentiment/'
    textblob = TextBlob(text)
    subj = textblob.sentiment.subjectivity

    # subjectivity analysis to exclude objective entries.
    if subj > 0.2:

        # API has an 80k char limit.
        if len(text) < 80000:
            
            try:
                req = requests.post(url, data={"text": text}, timeout=10)

                # perform sentiment analysis on OK response.
                if req.status_code == 200:
                    data = req.json()
                    pos = data.get('probability', {}).get('pos')

                    # only return pos value is numeric.
                    if isinstance(pos, int) or isinstance(pos, float):
                        return format(pos * 10, '.2f')

                    # otherwise return no data.
                    return

                # otherwise return no data.
                return

            except Exception as e:
                print("Please see error below.")
                print(e)

                # return no data if exception.
                return

        # return no data if subjectivity <= 0.2.
        return


def daily_affirmation(sentiment):
    """
    Returns a random daily affirmation based on the sentiment of a text entry.
    """
    
    # dict of affirmations to return.
    affirmations = {
        "vpos": ["Keep doing what you're doing!", 'You are amazing!',
                 "You're doing so great anyone who looks at you would be jealous.", 'You inspire me to be more like you!'],

        "pos": ['Even your hair is great today!', 'Slayyyyyyy!!!', "You're a smart cookie!", "You're an inspiration!"],

        "neutral": ['Today is a good day.', 'Go get yourself a cuppa and a biscuit, you need it!', "Small progress is still progress.", "Don't forget to enjoy the journey."],

        "neg": ["People don't slay everyday, and today is not your slay day. Make tomorrow your slay day.", 'Go grab a coffee.', 'All you need is the plan, the roadmap, and the courage to press on to your destination', 'Struggling is part of learning', "Mistakes don't make you less capable", "It is not a sprint, it is a marathon. One step at a time"],

        "vneg": ['Get yourself a Maccies today.', 'Tomorrow will be better!',
                 'Not everyday is gonna be as bad as today, forget about it... today never happened.', 'Failure is just another way to learn how to do something right', "Not everyday is gonna be as bad as today and not everyday are you going to eat your body weight in lasagne. So why not do it on the worse day of your life. Go on, eat your body weight in lasagne like no one's watching and forget about it... it never happened anyway."]
    }

    # return a randomly chosen sentiment.
    if sentiment <= 2:
        return random.choice(affirmations['vneg'])
    
    if sentiment > 2 and sentiment <= 4:
        return random.choice(affirmations['neg'])
    
    if sentiment > 4 and sentiment <= 6:
        return random.choice(affirmations['neutral'])
    
    if sentiment > 6 and sentiment <= 8:
        return random.choice(affirmations['pos'])
    
    if sentiment > 8 and sentiment <= 10:
        return random.choice(affirmations['vpos'])
    
    # if out of range.
    return 'Something has gone wrong.'
