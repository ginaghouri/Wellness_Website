
import webbrowser
from routes import app

def run():
    """
    Run the project.
    """

    print('Running localhost')

    # url that the Flask app runs on.
    url = 'http://127.0.0.1:5000'
    webbrowser.open(url)

    app.run()


if __name__ == '__main__':
    run()
