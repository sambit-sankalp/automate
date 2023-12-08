import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
import sys
import json

def trainModel():
    # Load the data
    data = pd.read_csv('generated_data.csv')  # Replace with your file path

    # Selecting features and target
    features = ['AdjustedPower', 'WinCount', 'SectorTotal', 'SectorActive', 'SectorFaults', 'SectorRecoveries']
    target = 'ReputationScore'

    # Splitting the data
    X = data[features]
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a pipeline with standardization and the model
    pipeline = Pipeline([
        ('scaler', StandardScaler()),  # Standardization
        ('rf', RandomForestRegressor(random_state=42))  # Random Forest Regressor
    ])

    # Hyperparameter tuning
    parameters = {
        'rf__n_estimators': [100, 200],
        'rf__max_depth': [None, 10, 20],
        'rf__min_samples_split': [2, 5]
    }
    grid_search = GridSearchCV(pipeline, parameters, cv=3, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train)

    # Best model
    best_model = grid_search.best_estimator_

    # Evaluate the model
    y_pred = best_model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    print(f"R² Score: {r2}")

    return best_model

def load_json_data(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data
    
def main(Address, AdjustedPower, WinCount, SectorTotal, SectorActive, SectorFaults, SectorRecoveries):
    best_model = trainModel()

    # new_miner = load_json_data(json_file)
    
    predicted_score = best_model.predict([ [AdjustedPower, WinCount, SectorTotal, SectorActive, SectorFaults, SectorRecoveries] ])
    print(f"Predicted Reputation Score for {Address}: {predicted_score[0]}")

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: python model.py <Address> <AdjustedPower> <WinCount> <SectorTotal> <SectorActive> <SectorFaults> <SectorRecoveries>")
        sys.exit(1)

    Address = sys.argv[1]
    AdjustedPower = sys.argv[2]
    WinCount = sys.argv[3]
    SectorTotal = sys.argv[4]
    SectorActive = sys.argv[5]
    SectorFaults = sys.argv[6]
    SectorRecoveries = sys.argv[7]

    main(Address, AdjustedPower, WinCount, SectorTotal, SectorActive, SectorFaults, SectorRecoveries)