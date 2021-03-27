#!/bin/bash
app='web_app_2'

ps -ef | grep $app | grep -v grep | awk '{print $2}' | xargs kill -9
