#!/bin/bash

ps -ef | grep hazmapi | awk '{print $2}' | xargs kill -9

nohup gunicorn --bind=0.0.0.0:5000 --workers=1 app --timeout 10 --name hazmapi --log-file - &
