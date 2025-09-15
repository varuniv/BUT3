import datetime
import pandas as pd
from IPython.display import display
from rich import print as rprint
from rich.syntax import Syntax

def assert_with_color(condition, message):
    if condition:
        pass
    else:
        # print colorful message to notebook using rich Syntax
        print_code_with_colors(message)

def print_code_with_colors(code):
    # Create a Syntax object with the code and Python lexer
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)

    # Display the colored code
    rprint(syntax)

# define HelperBase which can sho hint and solution
class HelperBase:
    _var = None
    _hint = None
    _solution = None

    def hint(self):
        if self._hint is not None:
            print_code_with_colors(self._hint)

    #print solution using pygments
    def solution(self):
        if self._solution is not None:
            print_code_with_colors(self._solution)

    def check(self, *args, **kwargs):
        self.solution()

#Step 1: define the function to evaluate the model
class CheckEvalFunction(HelperBase):
    _var = 'my_mae'
    _solution = """
def eval_DT(X_train, y_train, X_valid, y_valid, max_leaf_nodes):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model = model.fit(X_train, y_train)
    train_error = mean_absolute_error(y_train, model.predict(X_train))
    valid_error = mean_absolute_error(y_valid, model.predict(X_valid))
    return train_error, valid_error
"""
    _hint = """
# def eval_DT(X_train, y_train, X_valid, y_valid, max_leaf_nodes):
# define the model DecisionTreeRegressor
# fit the model with X_train, y_train
# calculate the mean_absolute_error for both train and valid data
# return train_error, valid_error
"""

# Step2 : charger les données et verifier le premier modele
class CheckFirstModel(HelperBase):
    _var = 'first_model'
    _solution = """
y = home_data.SalePrice
cols_with_missing = [col for col in home_data.columns if home_data[col].isnull().any()] 
X = home_data.drop(cols_with_missing, axis=1)
X.drop(['SalePrice'], axis=1, inplace=True)
X = X.select_dtypes(exclude=['object'])
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2,
                                                      random_state=0)
score = score_dataset(X_train, X_valid, y_train, y_valid)                                                      
"""
    _hint = """
# Utiliser home_data[col].isnull().any() pour savoir si une colonne contient des valeurs manquantes
# Utiliser drop pour supprimer les colonnes
"""
    def check(self, score):
        if score != 26055.69178082192:
            print_code_with_colors ("Expected score to be 26055.69178082192, but got {}".format(score))
            return
        print_code_with_colors ("The score is correct. Good job!")

# Step 3 Nous pouvons utiliser une boucle for pour comparer la précision des modèles construits avec différentes valeurs pour max_leaf_nodes.
import numpy as np
class CheckDifferentMaxLeafNodes(HelperBase):
    _var = 'scores'
    _solution = """
max_leaf_nodes = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
for i in max_leaf_nodes:
    res = eval_DT(X_train, y_train, X_valid, y_valid, max_leaf_nodes=i)
    train_errors.append(res[0])
    val_errors.append(res[1])
"""
    _hint = """
# Utiliser une boucle for pour parcourir les valeurs de max_leaf_nodes
# Utiliser eval_DT pour calculer les erreurs
"""

    def check(self, train_errors, val_errors):
        if 22612.1710363745 != np.mean(train_errors):
            print_code_with_colors ("Expected mean of train_errors to be 22612.1710363745, but got {}".format(np.mean(train_errors)))
            return
        if 25927.343935477118 != np.mean(val_errors):
            print_code_with_colors ("Expected mean of val_errors to be 25927.343935477118, but got {}".format(np.mean(val_errors)))
            return
        print_code_with_colors ("The errors are correct. Good job!")

# Step 4 : verifier score of the model when not use variables catégorielles and missing values
class CheckScoreWithoutCategorical(HelperBase):
    _var = 'score'
    _solution = """
# Pour simplifier, nous allons supprimer les colonnes avec des valeurs manquantes
cols_with_missing = [col for col in home_data.columns if home_data[col].isnull().any()] 
X = home_data.drop(cols_with_missing, axis=1)
X.drop(['SalePrice'], axis=1, inplace=True)

# Pour simplifier, nous allons selectionner les colonnes numeriques
numeric_cols = [cname for cname in X.columns if X[cname].dtype in ['int64', 'float64']]
X = X[numeric_cols]

X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2,
                                                      random_state=0)
score = score_dataset(X_train, X_valid, y_train, y_valid)
"""
    _hint = """
# Utiliser home_data[col].isnull().any() pour savoir si une colonne contient des valeurs manquantes
# Utiliser drop pour supprimer les colonnes
# Utiliser X[cname].dtype in ['int64', 'float64'] pour verifier si une colonne est numerique
"""

    def check(self, score):
        if 26055.69178082192 != score:
            print_code_with_colors ("Expected score to be 26055.69178082192, but got {}".format(score))
            return
        print_code_with_colors ("The score is correct. Good job!")

# Step 5 : verifier score with cross validation
class CheckScoreWithCrossValidation(HelperBase):
    _var = 'scores'
    _solution = """
def eval_cross_validation(X, y, max_leaf_nodes):    
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    scores = -1 * cross_val_score(model, X, y,
                                  cv=5,
                                  scoring='neg_mean_absolute_error')
    return scores.mean()

score = eval_cross_validation(X, y, 50)
"""
    _hint = """
# Definir le modele DecisionTreeRegressor avec max_leaf_nodes and random_state=0
# Utiliser cross_val_score pour calculer les erreurs
# return scores.mean()
"""

    def check(self, mean_score):
        if 25764.457771240024 != mean_score:
            print_code_with_colors ("Expected mean of scores to be 25764.457771240024, but got {}".format(mean_score))
            return
        print_code_with_colors ("The score is correct. Good job!")

# Step 6 : cross validation check for different max_leaf_nodes
class CheckCrossValidationForDifferentMaxLeafNodes(HelperBase):
    _var = 'scores'
    _solution = """
results = []
max_leaf_nodes = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80, 90, 100 ]
for i in max_leaf_nodes:
    results.append( eval_cross_validation(X, y, i))
    """
    _hint = """
# Utiliser une boucle for pour parcourir les valeurs de max_leaf_nodes
# Utiliser eval_cross_validation pour calculer les erreurs
"""

    def check(self, results):
        if 27142.27758757771 != np.mean(results):
            print_code_with_colors ("Expected mean of results to be 27142.27758757771, but got {}".format(np.mean(results)))
            return
        print_code_with_colors ("The errors are correct. Good job!")


step1 = CheckEvalFunction()
step2 = CheckFirstModel()
step3 = CheckDifferentMaxLeafNodes()
step4 = CheckScoreWithoutCategorical()
step5 = CheckScoreWithCrossValidation()
step6 = CheckCrossValidationForDifferentMaxLeafNodes()