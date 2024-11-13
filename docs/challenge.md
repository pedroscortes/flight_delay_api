# Flight Delay Prediction Challenge Documentation

## Overview
This project implements a machine learning service to predict flight delays at SCL airport. The implementation includes a trained model exposed through a REST API.

## Part I: Model Implementation

### Data Analysis
After analyzing the Jupyter notebook, I identified several key aspects:
1. The dataset contains flight information including scheduled and actual times
2. A delay is defined as a flight with more than 15 minutes difference between scheduled and actual times
3. Multiple models were tested:
   - XGBoost with/without feature selection
   - Logistic Regression with/without feature selection
   - Both models with and without class balancing

### Model Selection
I've chosen **Logistic Regression** with class balancing and feature selection as my final model for the following reasons:
1. Similar Performance:
   - Both models met test requirements
   - Logistic Regression showed comparable metrics to XGBoost
   - Test metrics achieved:
     - Class 0: Recall < 0.60, F1-score < 0.70
     - Class 1: Recall > 0.60, F1-score > 0.30

2. Model Simplicity:
   - Linear and more interpretable
   - Fewer hyperparameters to tune
   - Easier to maintain and debug

3. Resource Efficiency:
   - Lighter computational requirements
   - Faster training and inference
   - Smaller model size

4. Implementation Benefits:
   - Included in scikit-learn without additional dependencies
   - Simpler deployment process
   - Better suited for the binary classification nature of the problem

### Feature Engineering

The model uses the top 10 most important features:

```
features = [
    "OPERA_Latin American Wings", 
    "MES_7",
    "MES_10",
    "OPERA_Grupo LATAM",
    "MES_12",
    "TIPOVUELO_I",
    "MES_4",
    "MES_11",
    "OPERA_Sky Airline",
    "OPERA_Copa Air"
]
```

### Model Implementation Details

1. Preprocessing:

   - One-hot encoding for categorical variables
   - Feature selection based on importance
   - Standardization of numerical features


2. Class Balancing:

   - Implemented class weights to handle imbalanced data
   - Improved recall for minority class


3. Model Training:

   - Used standardized features
   - Applied class weights
   - Random state set for reproducibility


## Part II: API Implementation

### API Design

The API was implemented using FastAPI with the following endpoints:

1. Health Check:

```
@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK",
        "model_trained": model._model is not None
    }
```

2. Prediction Endpoint:

```
@app.post("/predict", status_code=200)
async def post_predict(data: PredictRequest) -> dict:
    return {"predict": predictions}
```

### Input Validation

Implemented comprehensive validation using Pydantic:

1. Month validation (1-12)
2. Flight type validation (N/I)
3. Operator validation (specific airlines)
4. Date format validation

### Error Handling

The API includes proper error handling for:

1. Invalid input data
2. Model not trained
3. Processing errors
4. Invalid data types

### Testing Results

The API implementation achieved:

1. 93% total code coverage
2. All test cases passing:

test_should_get_predict
test_should_failed_unkown_column_1
test_should_failed_unkown_column_2
test_should_failed_unkown_column_3

### Code Coverage Details:

```
Name                    Stmts   Miss  Cover
-------------------------------------------
challenge/__init__.py       3      1    67%
challenge/api.py           42      3    93%
challenge/model.py         30      1    97%
-------------------------------------------
TOTAL                      75      5    93%
```

