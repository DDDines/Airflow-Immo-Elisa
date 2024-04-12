import joblib
import os
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import OneHotEncoder


def train():
    
    if 'AIRFLOW_HOME' in os.environ:
        # Ambiente do Airflow
        base_directory = os.path.join(os.environ['AIRFLOW_HOME'], 'plugins', 'immo-eliza-scraper')
    else:
        # Ambiente local
        base_directory = os.path.join('C:', os.sep, 'Users', 'Julio', 'Desktop', 'BXL-Bouman-7', 'projects', '08-DE-immo-eliza-airflow', 'Airflow', 'dags', 'immo-eliza-scraper')

    # Define o caminho para o arquivo CSV limpo
    cleaned_csv_path = os.path.join(base_directory, 'Data', 'cleaned', 'cleaned.csv')

    # Carrega os dados
    data = pd.read_csv(cleaned_csv_path)

    # Define features to use
    num_features = [
        "construction_year",
        # "latitude",
        # "longitude",
        "total_area_sqm",
        "surface_land_sqm",
        "nbr_frontages",
        "nbr_bedrooms",
        "terrace_sqm",
        # "primary_energy_consumption_sqm",
        # "cadastral_income",
        "garden_sqm",
        "zip_code",
    ]

    fl_features = [
        "fl_terrace",
        "fl_open_fire",
        "fl_swimming_pool",
        "fl_garden",
        "fl_double_glazing",
        # "fl_floodzone",
        # "fl_furnished"
    ]

    cat_features = [
        "property_type",
        "subproperty_type",
        "locality",
        # "equipped_kitchen",
        #"kitchen_clusterized",
        # "state_building",
        #"state_building_clusterized",
        "epc",
        # "zip_code_text"
    ]

    # Split the data into features and target
    X = data[num_features + fl_features + cat_features]
    y = data["price"]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=405
    )

    # Impute numerical features missing values using SimpleImputer
    imputer = SimpleImputer(strategy="mean")
    imputer.fit(X_train[num_features])
    X_train[num_features] = imputer.transform(X_train[num_features])
    X_test[num_features] = imputer.transform(X_test[num_features])

    # Convert categorical columns with one-hot encoding using OneHotEncoder
    enc = OneHotEncoder(handle_unknown='ignore')
    enc.fit(X_train[cat_features])
    X_train_cat = enc.transform(X_train[cat_features]).toarray()
    X_test_cat = enc.transform(X_test[cat_features]).toarray()

    # Combine the numerical and one-hot encoded categorical columns
    X_train = pd.concat(
        [
            X_train[num_features + fl_features].reset_index(drop=True),
            pd.DataFrame(X_train_cat, columns=enc.get_feature_names_out()),
        ],
        axis=1,
    )

    X_test = pd.concat(
        [
            X_test[num_features + fl_features].reset_index(drop=True),
            pd.DataFrame(X_test_cat, columns=enc.get_feature_names_out()),
        ],
        axis=1,
    )

    # Instantiate the Gradient Boosting Regressor
    model = GradientBoostingRegressor(n_estimators=275, max_depth=10, random_state=555)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions on the train set and print scores
    y_pred_train = model.predict(X_train)
    r2_train = r2_score(y_train, y_pred_train)
    mae_test = mean_absolute_error(y_train, y_pred_train)
    mse_test = mean_squared_error(y_train, y_pred_train)
    print(f"Train set R² score: {r2_train}")
    print(f"Train set MAE: {mae_test}")

    # Make predictions on the test set
    y_pred_test = model.predict(X_test)
    r2_test = r2_score(y_test, y_pred_test)
    mae_test = mean_absolute_error(y_test, y_pred_test)
    mse_test = mean_squared_error(y_test, y_pred_test)
    print(f"Test set R² score: {r2_test}")
    print(f"Test set MAE: {mae_test}")

    # Save the model
    artifacts = {
        "features": {
            "num_features": num_features,
            "fl_features": fl_features,
            "cat_features": cat_features,
        },
        "imputer": imputer,
        "enc": enc,
        "model": model,
    }

    model_directory = os.path.join(base_directory, 'model')

    # Verifica se o diretório existe. Se não, cria o diretório.
    if not os.path.exists(model_directory):
        os.makedirs(model_directory)

    # Define o caminho completo para salvar o arquivo do modelo
    model_path = os.path.join(model_directory, 'Gradient_boost_artifacts.joblib')

    # Salva os artefatos do modelo
    joblib.dump(artifacts, model_path)
    print(f"Model and artifacts saved to {model_path}")


if __name__ == "__main__":
    train()
