# 💊 Chill Pill 💊
---

Hello and welcome to our project! We are Group 5, and this is Chill Pill - a Wellness Journal and Mood Tracker web app.

<p align="center">
  <img width="500" alt="Photo 1" src="https://github.com/sai-ma/G5-Chill-Pill/blob/main/static/images/photo1.png">
</p>

The primary goal of our project is to provide users with a user-friendly platform, in order to explore their emotions, promoting deeper self-understanding and emotional balance. Through the following key objectives our group project aims to achieve its overarching mission. 🧘‍♀️

With Chill Pill, you too can reach your best potential. 🎑

Try Chill Pill! It's completely *free*! 


> [!CAUTION]
> Our platform is designed to aid in emotional exploration and self-understanding. It is not a substitute for professional advice or treatment. Users engage at their own discretion, and while the platform aims to promote emotional balance, results cannot be guaranteed. This is a free service, subject to change, and users are encouraged to seek professional guidance for specific concerns.

---


## Features
#### 1. Web Interface - New Entry 🏠

<img width="1200" alt="Photo 5" src="https://github.com/sai-ma/G5-Chill-Pill/blob/main/static/images/photo5.png">

* The user can create journal entries of their daily feelings and/or moods where the entry is evaluated by an AI-based API which gives a sentiment analysis.
After your input is recorded, you will get the following confirmation message with a cute cat GIF to accompany it. 😺 Congratulations! Now we can explore our other functions.
   
> [!TIP]
> We incorporate data analysis on saved journal entries (discussed further below), therefore in order to make this step more colorful, please try to use non-objective, emotionally driven language to trigger our Sentiment API to give your entries high and low entries. 

#### 2. Web Interface - All Entries 📚
* We use a database to store and retrieve user entries and allow the user to: 
   - view all journal entries alongside their timestamps and mood (from the sentiment analysis).
     
     <img width="1200" alt="Photo 7" src="https://github.com/sai-ma/G5-Chill-Pill/blob/main/static/images/photo7.png">
     
   - update or delete older entries by clicking on the `UPDATE` or `DELETE` functions respectively.
     
     <img width="1200" alt="Photo 9" src="https://github.com/sai-ma/G5-Chill-Pill/blob/main/static/images/photo9.png">

#### 3. Web Interface - Mood Tracker 📚 📈 

<img width="1200" alt="Photo 13" src="https://github.com/sai-ma/G5-Chill-Pill/blob/main/static/images/msedge_RAILCuj3MQ.gif">

* Our mood tracker graph: 
    - illustrates mood (based on sentiment analyses of the user's journal entries) in the form of a graph.
    - displays the highs and lows of the user's mood with timestamps of these instances.
    - displays the user's average mood and their 3 highest and lowest mood entries with their corresponding timestamps.
      
> [!NOTE]
> You will be able to hover over the plots with your cursor, and zoom in as desired to a certain timeframe.

#### 4. Web Interface - The Team 👩‍💻

- Please feel free to click on the `The Team` category on our navigation bar to get to know us better!

<img width="1200" alt="Photo 14" src="https://github.com/sai-ma/G5-Chill-Pill/blob/main/static/images/msedge_Evp1vW7SM1.gif">

---

## Dependencies

This project utilizes several libraries and technologies, including:

- [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/)
- [TextBlob](https://textblob.readthedocs.io/en/dev/)
- [Plotly](https://plotly.com/python/)
- [Pandas](https://pandas.pydata.org/)


All dependencies can be viewed in the `requirements.txt` file and should be installed prior to running this project using the terminal command:

```bash
 pip install -r requirements.txt
```
 
---

## Installation Instructions

You will need:
1. Any web browser and a computer/laptop.
2. To install MongoDB following the instructions [here](https://www.mongodb.com/docs/manual/installation/).


Please clone the repository to the desired location on your local desktop using:
  
```bash
 git clone https://github.com/sai-ma/G5-Chill-Pill.git
```

Run the `main.py` file from the repository's root directory to launch the application:

```bash
 python main.py
```
OR alternatively:

```bash
 python3 main.py
```

> [!TIP]
> If the website does not load correctly, please return to the **[Dependencies](#Dependencies)** section and double-check all dependencies have been properly installed.

---

## About Us 👩‍💻

### Alex

- **Introduction**: My academic background is in Structural Engineering.
- **Project role(s**):  On this project I was part of the data team as well as managing the Jira board and taking minutes in the team meetings.
- **Personal links**: [Linkedin](https://www.linkedin.com/in/awojciechowska1/)

### Anu Bazarragchaa

- **Introduction**: Hey there! 😄 I'm Anu, currently transitioning into the world of software development. With a background in bioinformatics, now I'm venturing into coding. Ask me anything about  my Machine Learning projects on Drone Audio Detection or Spotify Music Recommendations!! 🖥️💻
- **Project role(s)**: 1/3rd of the Database team (*DELETE and UPDATE endpoints + unit testing, Sentiment plot base code contribution, Sentiment analysis design and endpoints' configuration*),  README.md (*Recommended workflow - Now merged with Dependencies and Features, The Team, and Additional resources* + Review, Presentation)
- **Personal links**: [Linkedin](https://www.linkedin.com/in/anu-bazarragchaa/) | [Github](https://github.com/anu-bazar)

### Chidimma

- **Introduction:** Hello! 😊 I’m a (quantum) chemist and an aspiring software developer. I really enjoy that when I fix one bug, several others spontaneously vanish! 🐞🤔
- **Project role(s):** Project lead, frontend team (UI design and development, UX development), backend team (server architecture and development, unit testing), database contributions (setup and create, read functionalities), codebase audit.
- **Personal links:** [LinkedIn](https://www.linkedin.com/in/chidimma-u-52256a177) | [GitHub](https://github.com/orchi-ia)

### Elizabeth

- **Introduction:** Hi I'm Lizzie!! Im a pharmacologist 💊 turned baker 🥐. I started coding as a hobby to make fun creative programs to incorperate my music too, now I am an aspiring software developer thanks to CFG!!
- **Project role(s):** Backend Team (server development, API implementation/Entry Analysis, affirmation generation), Frontend Contributions (Submission Page), Documentation Review Team (editing and finalising report)
- **Personal links:** [Linkedin](https://www.linkedin.com/in/elizabeth-dinh-/) | [Github](https://github.com/eldinh12)


### Gina    

- **Introduction**: I am Guru GanaSaki, a creative designer,filmmaker and multimedia artist learning software and web development by Code First Girls. I am also a traditionally-trained performer of Hindustani dances, music, yoga, organic farming and naturopathy.
- **Project role(s)**: Frontend team (created the UI animation interface of Chill Pill, added to the html, css and the README.md (Features, Dependencies and Instructions) in collaboration with our brilliant team of dev girls 🧞‍♀️🧙‍♀️🦹‍♀️🦸‍♀️👩‍🎓.
- **Personal links**: [Linkedin](https://www.linkedin.com/in/gina-rubik-25423923/) | [Github](https://github.com/ginarubik) | [Instagram](https://www.instagram.com/ganasakidesign/)

### Saima

- **Introduction**: Hi I'm Saima! I am aspiring to work in Cyber Security in the future, currently strengthening my coding skills through CFG. In the mean time, please tell me how to defeat Ganondorf in Tears of the Kingdom 🥲.
- **Project role(s)**: Database Team (building mood tracker functionality for our website and testing) , Documentation Review team (Editing and Reviewing final version of Group Report).
- **Personal links**: [Linkedin](https://www.linkedin.com/in/saima-k-ab1a04181/) | [Github](https://github.com/sai-ma)

---

