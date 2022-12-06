import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score

def cross_validate(model, X_train, y_train, metric, folds=5):
    """
    The function return results of cross validation given provided metric.
    
    Parameters
    ----------
    model: model
        Machine learning model to be cross validated
    X_train: DataFrame
       Dataframe with independent variables.
    y_train: array
       Dependent variable. 
    metric : str
        Metric to be calculated.
    folds : int, optional
        Number of folds to be used. The default is 5.
        
    Returns
    -------
    metric_scores: list of floats
        List of provided metric results per each fold
    """
        
    metric_scores = cross_val_score(model, X_train, y_train.values.reshape(-1, 1),                                                           
                              n_jobs=-1, scoring=metric)  
    msg = f"The mean Roc AUC score is {metric_scores.mean()} and the standard deviation is {metric_scores.std()}"
    print(msg)

    return metric_scores
        

def fit_model(model, X_train, y_train):
    """
    The function fits the  provided machine learning pipeline.
    
    Parameters
    ----------
    model: model
        Machine learning pipeline to be fitted.
    X_train: DataFrame
       Dataframe with independent variables.
    y_train: array
       Dependent variable. 
       
    Returns
    -------
    fitted_pipeline: sklearn pipeline
        Fitted machine learning pipeline.
       
    """
    
    fitted_pipeline = model.fit(X_train, y_train.values.reshape(-1, 1))    

    return fitted_pipeline  

def get_features_importance(fitted_model, X_train_columns):
    """
    The function gets and plots feature importance.
    
    Parameters
    ----------
    fitted_model: model
        Fitted machine learning model. 
    X_train_columns: list of str
        Column names of the independent variables used for the training.

    """
    
    feature_importances = pd.DataFrame({'Features': X_train_columns, 'Importance_Model_1': fitted_model.feature_importances_})
    feature_importances = feature_importances[feature_importances['Importance_Model_1'] != 0]
    feature_importances.reset_index(drop=True, inplace=True)
    
    top_15_feats = feature_importances.sort_values(by='Importance_Model_1',axis=0,ascending=False)['Features'].iloc[0:15]
    top_15_feats_scores = feature_importances.sort_values(by='Importance_Model_1',axis=0,ascending=False)['Importance_Model_1'].iloc[0:15]

    with plt.style.context('seaborn-poster'):
        sns.barplot(y=top_15_feats, x=top_15_feats_scores, orient='h', palette='coolwarm')
        plt.xlabel("\nFeatures Importance")
        plt.ylabel("Features\n")
        plt.title("Top 15 Importance Features\n")
   
            
def plot_confusion_matrix(fitted_model, X, y):
    
    """
    The function evaluates predictions against provided values.
    The results are displayed as roc_auc score, f1 score and confusion matrix.
    
    Parameters
    ----------
    fitted_model: model
        Machine learning pipeline to be evaluated.
    X: DataFrame
       Dataframe with independent variables.
    y: array
       Dependent variable. 
       
    """
           
    predictions = fitted_model.predict(X)
    
    ConfusionMatrix = confusion_matrix(y, predictions)
    RocAuc = roc_auc_score(y, predictions) 
    f1score = f1_score(y, predictions)
    ConfusionMatrixDisplay(ConfusionMatrix, display_labels = [0,1]).plot(values_format='d')
    plt.show()
    print('ROC AUC on provided set is: ', RocAuc)
    print('F1 score on provided set is: ', f1score)
    print()
    
def plot_confusion_matrix_comparison(fitted_model_a, fitted_model_b, X, 
                                      X_enhanced, y):
    
    """
    The function evaluates predictions against provided values.
    The results are displayed as roc_auc score, f1 score and confusion matrix.
    
    Parameters
    ----------
    fitted_model_a: model
        Machine learning pipeline to evaluate.
    fitted_model_b: model
            Machine learning pipeline to evaluate.
    X: DataFrame
       Dataframe with independent variables.
    X_enhanced: DataFrame
       Dataframe with independent variables.
        
    y: array
       Dependent variable. 
       
    """
    
    for fitted_model, train_set in zip([fitted_model_a, fitted_model_b], [X, X_enhanced]):
           
        predictions = fitted_model.predict(train_set)
        
        ConfusionMatrix = confusion_matrix(y, predictions)
        RocAuc = roc_auc_score(y, predictions) 
        f1score = f1_score(y, predictions)
        ConfusionMatrixDisplay(ConfusionMatrix, display_labels = [0,1]).plot(values_format='d')
        plt.show()
        print('ROC AUC on provided set is: ', RocAuc)
        print('F1 score on provided set is: ', f1score)
        print()
    
def compare_models(model_names, cv_results):
    """
    Plots results of cross validation for each provided model for comparisson.
    
    Parameters
    ----------
    model_names: list of str
        List of name(s) of the provided pipeline(s)
    cv_results: list of lists of floats
        List of cross validation results of each pipeline
        
    """
    
    # if the model name provided is string make it a list
    if type(model_names) != list:
        model_names = [model_names]

    # if only one list of floats is provided make it item of list  
    if type(cv_results[0]) != np.ndarray:
        cv_results = [cv_results]

    for model_name, cv_result in zip(model_names, cv_results):
        msg = f"{model_name}: The mean Roc AUC score is {cv_result.mean()} and the standard deviation is {cv_result.std()}"
    
        print(msg)
        
    # Compare pipelines
    fig = plt.figure(figsize = (12, 8))
    fig.suptitle('Pipelines Comparison')
    ax = fig.add_subplot(111)
    plt.boxplot(cv_results)
    ax.set_xticklabels(['Model A', 'Model B'])
    plt.show()   