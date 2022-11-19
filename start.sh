#!/usr/bin/bash

export FLASK_APP=services.rest.chatbot
export FLASK_ENV=development

flask run &
