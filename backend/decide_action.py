from google import genai
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal
from predictions import make_pred
from db_action import get_historical_data

load_dotenv()

class Action(BaseModel):
    action: Literal["db", "prediction"] = Field(description="action required to take from the given query")
    rest_id: int = Field(description="the restaurant id to forecast the data, 0 if not provided")
    orders_date: str = Field(description="date for the forecast in the format YYYY-MM-DD, NA if not provided")
    promo_flag: int = Field(description="promo id given in the query, -1 if not provided")
    sql_query: str = Field(description="SQL query for retrieving the orders, insufficient data if the data is less")


key = os.getenv("API_KEY")
client = genai.Client(api_key = key)


def action(query:str):
    
    enhanced_query = query + """
            The name of the table is orders with columns restaurant_id(numeric), order_date(date), order_id, 
            retrieve count of the orders for each in the given range, for the given restaurant id for the given period, 
            generate the sql query if the user query consists/asks for the historical data in the db.
            IMPORTANT: If the query is about historical data or past orders, set action to 'db'.
            If the query is about forecasting, predicting, or estimating future orders, set action to 'prediction'.
        """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=enhanced_query,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": Action.model_json_schema(),
            },
        )

        res = Action.model_validate_json(response.text)
        print(f"Action decision: {res.action}")
        print(f"Details: rest_id={res.rest_id}, date={res.orders_date}, promo={res.promo_flag}")
        
        if res.action == 'prediction':
            print("Executing prediction action")
            res1 = make_pred({
                "restaurant_id":res.rest_id,
                "target_date": res.orders_date,
                "promo_flag": res.promo_flag
            })
            return res1
        else:
            print(f"Executing database action with query: {res.sql_query}")
            return get_historical_data(res.sql_query)
    except Exception as e:
        print(f"Error in action function: {str(e)}")
        return {"error": f"Failed to process action: {str(e)}", "chartdata": {}}