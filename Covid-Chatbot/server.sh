rasa run --endpoints endpoints.yml --connector socketio --credentials credentials.yml --port 5005 --cors "*" --enable-api
rasa run actions
python3 app.py


