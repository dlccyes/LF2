# LF2 - Easy Classroom Monitoring Tool for Teachers

**Go to the [wiki](https://github.com/dlccyes/LF2/wiki) to see full documentation**

See it in action!  

- <http://lf2-classroom-monitor.us-east-2.elasticbeanstalk.com/>
- <http://flask-env.eba-ts5yjdi9.us-east-2.elasticbeanstalk.com/> (backup)
- <https://classroom-helper-lf2.herokuapp.com/> (Heroku backup)

## What is this?

By placing a Jetson Nano with a camera in front of the classroom, you'll be able to monitor your classroom with a web dashboard. 

The program on Jetson Nano will take a shot periodically, do face & emotion recognition, and record the result to database. The webapp hosted on AWS will then pick up the new data and update the dashboard. From the dashboard, you'll know how many students have come to your class, and the general vibe of the classroom. With the positivity vs. time graph, you'll even know if your joke works!

## Tech Stack

- Web: Flask & Vue
- Web hosting: AWS EC2 (with Elastic Beanstalk)
- Database: AWS DynamoDB
- Live Capuring: Jetson Nano
- Face Recognition: Jetson Nano
- Emotion Recognition: AWS Rekognition

## System Architecture

![sys arch](resources/sys_arch.png)

## Emotion Recognition

![](https://i.imgur.com/GSGXw4c.png)

### Types of Emotions

- SURPRISED
- HAPPY
- CALM
- CONFUSED
- SAD
- ANGRY
- FEAR
- DISGUSTED
- UNKNOWN

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

## How to run the webapp locally?

### Download the codes

```
git clone https://github.io/dlccyes/LF2.git
```

### Prepare the environment

**Supply environment variables**

```
cp .env_bak .env
```
Fill `.env` with the correct AWS credentials. (Never commit it.)

**Install Python dependencies**

```
pip3 install -r requirements.txt
```

**Install Node dependencies**

```
cd vue
npm install
```

### Build the Vue frontend

```
cd vue
npm run build
```

### Run the Flask server

```
python3 application.py
```

And you're done! Head to <http://127.0.0.1:5000> to see the dashboard.

## How to run the register and the in-class monitor on Jetson Nano?
### Devices
- [Jetson Nano](https://www.nvidia.com/zh-tw/autonomous-machines/embedded-systems/jetson-nano/)
- [Raspberry Pi Camera V2](https://www.raspberrypi.com/products/camera-module-v2/)
- [Scanner](https://www.amazon.com/usb-scanner/s?k=usb+scanner)

### Install project dependencies
#### gRPC-with-protobuf
```
# Install protobuf compiler
$ sudo apt-get install protobuf-compiler

# Install buildtools
$ sudo apt-get install build-essential make

# Install grpc packages
$ pip3 install -r grpc_requirements.txt
```

#### AWS SDK for Python

**Python dependencies**

```
# Install boto3
$ pip3 install boto3

# Install dotenv
$ pip3 install python-dotenv

```

Rename `.env_bak` to `.env` in the project root and supply it with the correct credentials for this script to work.

**AWS credentials**

Install & configure AWS CLI or supply the credentials directly as follow

```
# Setup your host environment
$ cd ~
$ mkdir .aws && cd .aws
$ vim credentials
$ vim config
```

Add access key in the credentials file and region in the config file.

#### Face Recognition
```
# Install the face_recognition package on Jetson Nano
$ sudo apt-get install python3-pip cmake libopenblas-dev liblapack-dev libjpeg-dev
$ git clone https://github.com/JetsonHacksNano/installSwapfile
$ ./installSwapfile/installSwapfile.sh

$ wget http://dlib.net/files/dlib-19.17.tar.bz2 
$ tar jxvf dlib-19.17.tar.bz2
$ cd dlib-19.17
# Remove "forward_algo = forward_best_algo;" in dlib/cuda/cudnn_dlibapi.cpp

$ sudo python3 setup.py install
$ sudo pip3 install face_recognition
```

```
# Install Tensorflow on Jetson Nano
$ pip3 install Cython
$ pip3 install numpy
$ pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp36-cp36m-linux_aarch64.whl
```

#### Scanner
```
# Install evdev
$ pip3 install evdev
```

Change the event number to the that corresponding to the scanner in `jetson-nano/scanner.py`

### Usage
Run the gRPC server on your Jetson Nano
```
$ python3 jetson-nano/server.py
```

Register with student ID & photo
```
sudo python3 jetson-nano/register.py
```

In-class monitor
```
python3 jetson-nano/inclass_monitor.py
```
