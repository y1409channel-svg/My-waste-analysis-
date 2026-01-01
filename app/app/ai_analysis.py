import pandas as pd
from sklearn.linear_model import LinearRegression

def analyze_waste(df: pd.DataFrame):
    total = df["total"].sum()
    usable = df["usable"].sum()
    unusable = df["unusable"].sum()

    saved_percent = (usable / total * 100) if total > 0 else 0

    model = LinearRegression()
    model.fit(df[["total"]], df["usable"])
    predicted_usable = model.predict([[100]])[0]

    return {
        "total_waste_received": round(total, 2),
        "usable_waste": round(usable, 2),
        "unusable_waste": round(unusable, 2),
        "waste_saved_percent": round(saved_percent, 2),
        "ai_prediction_usable_from_100kg": round(predicted_usable, 2)
    }
