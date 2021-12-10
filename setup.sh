#!/usr/bin/env bash

pip -q install gym
sudo apt-get -qq update
sudo apt-get -qq -y install xvfb freeglut3-dev ffmpeg> /dev/null
sudo apt-get -qq install xvfb
pip -q install pyvirtualdisplay
pip -q install pyglet
pip -q install pyopengl
sudo apt-get -qq install swig
pip -q install box2d box2d-kengz
pip -q install pybullet