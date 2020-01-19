#!/bin/bash

docker build -t joachimveulemans/music-instruments-classifier:frontend ./frontend/

docker build -t joachimveulemans/music-instruments-classifier:backend ./backend/
