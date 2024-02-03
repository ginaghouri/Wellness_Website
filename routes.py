
from flask import render_template, request, redirect, url_for
from datetime import datetime as dt
from config import app, journal

from utils import sentiment_analysis, daily_affirmation


# home app route.
@app.route('/')
def home():
    """
    Journal entry page.
    """
    return render_template('index.html')


@app.route('/static/images')
def serve_static(filename):
    """
    Route to serve static files.
    """
    
    return app.send_static_file(filename)


@app.route('/journal', methods = ['POST'])
def add_entry():
    """
    Add an entry to the DB.
    """
    
    # error handling to check for an entry body.
    try:
        entry = request.form.get('entry')

        if not entry:
            # if entry body is nonexistent.
            result = 'Error: We could not save this entry. Please ensure there is text in the journal entry.'

            return render_template('index.html', result=result)
        
        sentiment = sentiment_analysis(entry)
        journal.manager.create(entry, sentiment)
        result = 'New journal entry added!'

        # filters for non-None sentiments.
        if isinstance(sentiment, str):
            daily_affirm = daily_affirmation(float(sentiment))

            # redirects to submission page.
            return redirect(url_for('submission_page', result=result, daily_affirm=daily_affirm))
        
        # otherwise, no daily affirmation/sentiment.
        return redirect(url_for('submission_page', result=result))
            
    # if 'entry' key doesn't exist.
    except KeyError as e:
        print("Please see error below.")
        print(e)
        
        result = 'Error: We could not save this entry. \n'
        return render_template('index.html', result=result)


@app.route('/submission')
def submission_page():
    """
    Returns a daily affirmation on the submission page.
    """
    
    # get args for the template.
    result = request.args.get('result')
    daily_affirm = request.args.get('daily_affirm')

    return render_template('submission.html', result=result, daily_affirm=daily_affirm)


@app.route('/entries', methods=['GET'])
def entries():
    """
    Retrieves all entries from the DB to read to the web page.
    """

    entries_data = journal.manager.read_all()

    # convert to an iterable for iterating in HTML.
    if isinstance(entries_data, dict):
        entries_data = [entries_data]

    # return the web page that has all entries on it.
    return render_template('entries.html', entries_data=entries_data)


@app.route('/entries/<_id>', methods=['GET'])
def find_entry(_id):
    """
    Retrieves an entry from the DB to read to the web page.
    """

    entry_data = journal.manager.read_one(_id)

    # convert to an iterable for iterating in HTML.
    if isinstance(entry_data, dict):
        entry_data = [entry_data]

    # return the web page that has the entry on it.
    return render_template('entry.html', entry_data=entry_data)


@app.route('/delete/<entry_id>', methods=['POST'])
def delete_entry(entry_id):
    """
    Deletes an entry, redirects to the entries page.
    """
    journal.manager.delete(entry_id)

    # return to entries page.
    entries_data = journal.manager.read_all()

    if isinstance(entries_data, dict):
        entries_data = [entries_data]

    return redirect(url_for('entries', entries_data=entries_data))


@app.route('/update/<entry_id>', methods=['POST'])
def update_entry(entry_id):
    """
    Updates an entry, redirects to the entries page.
    """

    try:
        # get the updated details.
        entry = request.form.get('entry')

        if not entry:
            # otherwise, throw an error template and return to the og entry.
            result = '404 Error: Entry body not found.'
            entry_data = journal.manager.read_one(entry_id)

            return render_template('entry.html', entry_data=entry_data, result=result)
        
        time = dt.now().strftime("%d/%m/%Y %H:%M:%S")

        # update sentiment analysis on updated entry.
        sentiment = sentiment_analysis(entry)

        update_data = {
            'body': entry,
            'sentiment': sentiment,
            'last timestamp': time
        }
        
        journal.manager.update(entry_id, update_data)

        # check if the entry was updated successfully.
        query = {'body': entry,
                'last timestamp': time}

        updated = journal.manager.check_one(query)

        # if entry has been updated, redirect.
        if updated:
            entries_data = journal.manager.read_all()

            if isinstance(entries_data, dict):
                entries_data = [entries_data]

            return redirect(url_for('entries', entries_data=entries_data))
    
    # if 'entry' key doesn't exist.
    except KeyError as e:
        print("Please see error below.")
        print(e)
        
        result = '404 Error: We are unable to get your journal entry.'
        entry_data = journal.manager.read_one(entry_id)

        return render_template('entry.html', entry_data=entry_data, result=result)
        

@app.route('/moodtracker')
def mood_plot():
    """
    Generates sentiment plot and analysis.
    """
    
    # get the plot and sentiment analytics.
    plot_html = journal.mood.plot_mood()
    lowest_posts = journal.mood.min_sentiments()
    avg_sentiment = journal.mood.av_sentiment()
    highest_posts = journal.mood.max_sentiments()

    # render web page.
    return render_template('mood.html', plot_1=plot_html, lowest=lowest_posts, last_seven_avg_sentiment=avg_sentiment, highest = highest_posts)


@app.route('/team')
def meet_team():
    """
    Team page.
    """
    
    return render_template('team.html')
