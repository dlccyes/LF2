# How to run the register and the in-class monitor on Jetson Nano?
## Devices
- [Jetson Nano](https://www.nvidia.com/zh-tw/autonomous-machines/embedded-systems/jetson-nano/)
- [Raspberry Pi Camera V2](https://www.raspberrypi.com/products/camera-module-v2/)
- [Scanner](https://www.amazon.com/usb-scanner/s?k=usb+scanner)

## Install project dependencies
### gRPC-with-protobuf
```
# Install protobuf compiler
$ sudo apt-get install protobuf-compiler

# Install buildtools
$ sudo apt-get install build-essential make

# Install grpc packages
$ pip3 install -r grpc_requirements.txt
```

### AWS SDK for Python
```
# Install boto3
$ pip3 install boto3

# Install dotenv
$ pip3 install python-dotenv

Rename `.env_bak` to `.env` in the project root and supply it with the correct credentials for this script to work.

# Setup your host environment
$ cd ~
$ mkdir .aws && cd .aws
$ vim credentials
$ vim config

Add access key in the credentials file and region in the config file.
```

### Face Recognition
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

### Scanner
```
# Install evdev
$ pip3 install evdev

Change the event number to the that corresponding to the scanner in jetson-nano/scanner.py
```

## Usage
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
