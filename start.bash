#!/bin/bash
chroma run --path Resource/chroma_db2 --port 1224 &
while ! nc -z localhost 1224; do 
  sleep 1
done 
gunicorn -w 4 'main:app'
