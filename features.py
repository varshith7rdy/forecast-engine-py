import pandas as pd

feature_df = pd.read_csv("feature_store.csv")


def build_features(restaurant_id:int, target_date:str, promo_flag=0):

    target_date = pd.to_datetime(target_date)

    feature_df['date'] = pd.to_datetime(feature_df['date'])

    hist = feature_df[
        (feature_df['restaurant_id'] == restaurant_id) &
        (feature_df['date'] < target_date)
    ].sort_values('date')

    if len(hist) < 30:
        raise ValueError("Not enough history for feature generation")
    lag_1 = hist['orders'].iloc[-1]
    lag_7 = hist['orders'].iloc[-7]
    lag_14 = hist['orders'].iloc[-14]
    lag_30 = hist['orders'].iloc[-30]


    rolling_7 = hist['orders'].iloc[-7:].mean()
    rolling_30 = hist['orders'].iloc[-30:].mean()


    day_of_week = target_date.dayofweek
    week_of_year = target_date.isocalendar().week
    month = target_date.month


    avg_rating = hist['avg_rating'].iloc[-1]
    weather_index = hist['weather_index'].iloc[-1]

    features = pd.DataFrame([{
        'avg_rating': avg_rating,
        'day_of_week': day_of_week,
        'week_of_year': week_of_year,
        'month': month,
        'lag_1': lag_1,
        'lag_7': lag_7,
        'lag_14': lag_14,
        'lag_30': lag_30,
        'rolling_7': rolling_7,
        'rolling_30': rolling_30,
        'promo_flag': promo_flag,
        'weather_index': weather_index
    }])

    features = features.astype(float)
    print("Features are created!!")
    return features
