# LF2 - Learning Feedback from Face

Network Lab Final Project

See it in action!  

- <http://flask-env.eba-ts5yjdi9.us-east-2.elasticbeanstalk.com/>  
- <https://classroom-helper-lf2.herokuapp.com/> (herkou backup ver.)

## Tech Stack

- Web: Flask & jQuery
- Web hosting: AWS EC2 (with Elastic Beanstalk)
- Database: AWS DynamoDB
- Live Capuring: Jetson Nano
- Face & Emotion Recognition:

## How to update face & emotion recognition data to the database?

### Download the codes

```
git clone https://github.io/dlccyes/LF2.git
```

### Prepare the environment

```
cp .env_bak .env
```
Fill `.env` with the correct AWS credentials. (Never commit it.)

### Update database with your data

The functions for updating data is in [`jetson-nano/update_db.py`](jetson-nano/update_db.py). 

So you can put the face or emotion recognition code in `jetson-nano` and `import update_db.py` to use it.

There are 2 functions in it. 

The input for `log_emotion` is a 2D list. Each element consists of an emotion (string) and its confidence (integer). There can be duplicate emotions. Sample intpu: `[['happy', 0.98], ['neutral', 0.87], ['neutral', 0.32]]`.

The input for `log_attendance` is a 1D list. Each element is a unique student id (string). Sample input: `['B08901000', 'B08901002', 'B08901001']`.

Please refer to [`jetson-nano/generate_data.py`](jetson-nano/generate_data.py) for sample usage.

## Emotion Recognition

![](https://i.imgur.com/GSGXw4c.png)

### Types of Emotions

- surprise
- happy
- neutral
- sad
- fear
- disgust
- contempt
- anger

## Face Recognition

![](https://i.imgur.com/7W5aEJm.png)