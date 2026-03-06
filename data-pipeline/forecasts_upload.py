# backend/uploader_script.py
import pandas as pd
from database import get_db_engine

file_path = "../logs/predictions_buffer.jsonl"

def run_batch_upload():
    engine = get_db_engine()
    df = pd.read_json(file_path, lines=True)
    
    df.to_sql('forecasts', engine, if_exists='append', index=False)
    print("Batch upload successful!")
    with open(file_path, 'w') as f:
        f.write("")
