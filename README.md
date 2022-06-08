# LF2 - Classroom Helper for Teachers

2022 Network Lab Final Project

See it in action!  

- <http://flask-env.eba-ts5yjdi9.us-east-2.elasticbeanstalk.com/> 
- <https://classroom-helper-lf2.herokuapp.com/> (Heroku backup ver.)


## What is this?

By placing a Jetson Nano with a camera in front of the classroom, you'll be able to monitor your classroom with a web dashboard. 

The program on Jetson Nano will take a shot periodically, do face & emotion recognition, and record the result to database. The webapp hosted on AWS will then pick up the new data and update the dashboard. From the dashboard, you'll know how many students have come to your class, and the general vibe of the classroom. With the positivity vs. time graph, you'll even know if your joke works!

## Tech Stack

- Web: Flask & Vue
- Web hosting: AWS EC2 (with Elastic Beanstalk)
- Database: AWS DynamoDB
- Live Capuring: Jetson Nano
- Face & Emotion Recognition: PyTorch

## System Architecture

<!-- ![](https://i.imgur.com/MZxVNtl.png) -->
![](resources/sys_arch.png)

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

## Frontend Dashboard

There are two versions of frontend available. The default one is written in Vue, and the other is written in vanilla HTML/JavaScript/CSS + jQuery, rendered with Flask's template. You can switch to the latter one by setting `VUE` to `false` (or just remove it) in your [environment variables](.env_bak).

There are many features:

**Theme switcher**

You can toggle the theme by clicking the moon button at the top right.

**Time slider**

You can easily change the scope of time to watch by dragging the slider at the top of the page.

**Attendance**

You can see the last recorded attendance as well as the attendance vs. time chart to see the attendance of your classroom over time.

**Emotion**

You can see the positivity of the classroom over time as well as the emotion cloud to get an idea of the general vibe of the classroom in the scope of time you selected.

**Specific students**

Apart from seeing the overall condition of the classroom, you can also head to each student's page to see their attendance record.

![](https://i.imgur.com/yXz8QOK.png)