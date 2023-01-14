__all__ = ['train_model', 'predict_model']

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import numpy as np
import pickle
import os

##################### CONSTANTS #################
MODEL_FILE='random_forest.pkl'


# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True]
# Create the random grid
random_grid_random = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}


# Create the parameter grid based on the results of random search 
param_grid_grid = {
    'bootstrap': [True],
    'max_depth': [80, 90, 100, 110],
    'max_features': [2, 3],
    'min_samples_leaf': [3, 4, 5],
    'min_samples_split': [8, 10, 12],
    'n_estimators': [100, 200, 300, 1000]
}



def split_data(X, y, test_size=0.05):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y, test_size=test_size, random_state=42
    )

    print(f'''
    Training data shape:
    X_train: {X_train.shape}
    y_train: {y_train.shape}
    X_test : {X_test.shape}
    y_test : {y_test.shape}
    ''')
    return X_train, X_test, y_train, y_test



def enable_cross_validation(model, X_train, y_train):
    return cross_validate(model, X_train, y_train, cv=10, scoring=["accuracy", "precision", "recall"])



# print(f'''
#     Random search:
#     {random_grid_random}
#     ----------------------------
#     Grid Search:
#     {param_grid_grid}
# ''')


def save_model(model, save_path:str):
    if not os.path.exists(save_path):
        raise Exception(f'''random_forest.save_model(): save path does not exist:
        {save_path}
        ''')
    with open(os.path.join(save_path, MODEL_FILE), 'wb') as f:
        pickle.dump(model, f)


def load_model(model_path:str):
    if not os.path.exists(model_path):
        raise Exception(f'''random_forest.save_model(): save path does not exist:
        {model_path}
        ''')
    with open(os.path.join(model_path, MODEL_FILE), 'rb') as f:
        return pickle.load(f)



def train_model(config, X, y, test_size=0.05, search_type='grid'):
    '''
    Train the RandomForestClassifier
    Parameters:
        @config dict: Configuration dictionary
        @X np array : Training Input
        @y np array : Training target variable
        @test_size  : proportion of test size
        @search_type: grid or random
    '''
    # Use the random grid to search for best hyperparameters
    # First create the base model to tune
    rf = RandomForestClassifier()
    # Random search of parameters, using 3 fold cross validation, 
    # search across 100 different combinations, and use all available cores
    params_search, search_class = (param_grid_grid, GridSearchCV) if search_type == 'grid' else (random_grid_random, RandomizedSearchCV)

    print(f'''
    -------------- Search by {search_type} -----------------
    Parameters:
    {params_search}
    ''')

    parameters = {'param_grid':params_search, 'estimator': rf, 'scoring':'accuracy', 'n_jobs':-1, 'cv':3, 'return_train_score':True } \
     if search_type == 'grid' else \
     {'param_distributions':params_search, 'estimator': rf, 'scoring':'accuracy', 'n_jobs':-1, 'cv':3, 'return_train_score':True, 'n_iter':100 }
    

    rf_best = search_class(**parameters)
    # Fit the random search model
    print(f'''
    Model Description before training:
    {rf_best}
    ''')

    X_train, X_test, y_train, y_test = split_data(X, y, test_size=test_size)
    rf_best.fit(X_train, y_train)

    print(f'''

    Model Description post training:
    -------------------------------
    Best Estimator: {rf_best.best_estimator_}
    Best Score    : {rf_best.best_score_}
    Best Params   : {rf_best.best_params_}

    ''')

    print(f'''
    Classes in the estimators:
    {rf_best.best_estimator_.classes_}
    ''')

    print('--------------- Training Report on test data --------------------')
    print(classification_report(y_test, rf_best.predict(X_test), target_names=rf_best.best_estimator_.classes_))
    print('--------------- Training Report on test data --------------------')
    # Save the model
    save_model(rf_best, os.getenv('PREPROCESS_PATH'))
    



def predict_model(config, X):
    '''
    Predict from RandomForestClassifier
    Parameters:
        @config dict: Configuration dictionary
        @X np array : Training Input
    '''
    model = load_model(os.getenv('PREPROCESS_PATH'))
    print(f'''
        Prediction is: {model.predict(X)}
    ''')
    return model.predict_proba(X)[0], model.best_estimator_.classes_, model.predict(X)[0]



# def evaluate(model, test_features, test_labels):
#     predictions = model.predict(test_features)
#     errors = abs(predictions - test_labels)
#     mape = 100 * np.mean(errors / test_labels)
#     accuracy = 100 - mape
#     print('Model Performance')
#     print('Average Error: {:0.4f} degrees.'.format(np.mean(errors)))
#     print('Accuracy = {:0.2f}%.'.format(accuracy))
    
#     return accuracy





