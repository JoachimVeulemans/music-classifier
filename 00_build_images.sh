#!/bin/bash

docker build -t music-instruments-classifier:frontend ./frontend/

docker build -t music-instruments-classifier:backend ./backend/
