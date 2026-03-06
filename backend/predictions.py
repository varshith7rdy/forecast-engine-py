from features import build_features
from pydantic import BaseModel
import math
import joblib
from logger import log_predictions

model = joblib.load("lightgbm_orders_v1.pkl")

def make_pred(request):

    print("Request:", request)

    try:        
        input_features, chardata = build_features(
            request["restaurant_id"], 
            request["target_date"],
            request["promo_flag"]
        )

        if hasattr(model, 'booster_'):
            prediction = model.booster_.predict(input_features)
        else:
            prediction = model.predict(input_features)

        print("Prediction complete")

        data = {
            "restaurant_id": request["restaurant_id"],
            "target_date": request["target_date"],
            "predicted_orders": math.ceil(prediction[0]),
        }

        log_predictions(data)

        data['chartdata'] = chardata
 
        return data
        
    except ValueError as e:
        return {"error": str(e), "status": 400}
    except Exception as e:
        print("error", "Prediction failed", "detail", str(e), "status", 500)
        return {"error": "Prediction failed", "detail": str(e), "status": 500}