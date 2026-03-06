from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL)

def get_historical_data(query):

    try:
        df = pd.read_sql(query, engine)
        
        if df.empty:
            return {"error": "No data found for the given query", "chartdata": {}}
        
        columns = df.columns.tolist()
        
        date_col = None
        order_col = None
        
        for col in columns:
            if 'date' in col.lower():
                date_col = col
            if 'count' in col.lower() or 'orders' in col.lower() or col.lower().endswith('count'):
                order_col = col
        
        if date_col is None:
            date_col = columns[0]
        
        if order_col is None:
            order_col = columns[1] if len(columns) > 1 else columns[0]
        
        chartdata = {}
        for idx, row in df.iterrows():
            date_str = str(row[date_col]).split()[0] if pd.notna(row[date_col]) else str(row[date_col])
            order_count = int(row[order_col]) if pd.notna(row[order_col]) else 0
            chartdata[date_str] = order_count
        
        return {
            "chartdata": chartdata,
            "status": "success",
            "total_records": len(df)
        }
    
    except Exception as e:
        print(f"Database error: {e}")
        return {"error": str(e), "chartdata": {}}