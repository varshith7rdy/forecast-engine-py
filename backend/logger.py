import os
import datetime
import json
from pathlib import Path

p = Path('../logs/predictions_buffer.jsonl')

def log_predictions(data):

    data['logged_at'] = str(datetime.datetime.now())
    print(data['logged_at'])

    with open(p, "a") as f:
        f.write(json.dumps(data) + "\n")

    print("Logging completed")