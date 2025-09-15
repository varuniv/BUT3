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
        raise self.solution()

#step1 : check the score_dataset function 
class CheckScoreDataset(HelperBase):
    _var = 'score_dataset'
    _hint = """
# Define the function to measure quality of an approach
# def score_dataset(X_train, X_test, y_train, y_test):
#     model = LinearRegression()
#     fit le modele avec X_train, y_train
#     obtenir les predictions avec model.predict et X_test
#     return mean_absolute_error de y_test et predictions"""
    _solution = """
from sklearn.metrics import mean_absolute_error
def score_dataset(X_train, X_test, y_train, y_test):
    model = LinearRegression()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return mean_absolute_error(y_test, preds)"""

    def check(self, score):
        if score != 29680.799555678055 :
            print_code_with_colors ("Expected score to be 29680.799555678055 , but got {}".format(score))
            return
        
        print_code_with_colors ("score = {} looks good. Good job!".format(score))

#step 2, check code when we use all the columns
class CheckAllColumns(HelperBase):
    _var = 'all_X'
    _solution = """
predictors = home_data.drop(['SalePrice'], axis=1)
X = predictors.select_dtypes(exclude=['object'])
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2,
                                                      random_state=0)
"""
    _hint = ""

    def check(self, X_train, X_valid, y_train, y_valid):
        if X_train.shape != (1168, 37):
            print_code_with_colors ("Expected X_train to have shape (1168, 37), but got {}".format(X_train.shape))
            return
        if X_valid.shape != (292, 37):
            print_code_with_colors ("Expected X_valid to have shape (292, 37), but got {}".format(X_valid.shape))
            return
        if y_train.shape != (1168,):
            print_code_with_colors ("Expected y_train to have shape (1168,), but got {}".format(y_train.shape))
            return
        if y_valid.shape != (292,):
            print_code_with_colors ("Expected y_valid to have shape (292,), but got {}".format(y_valid.shape))
            return
        
        print_code_with_colors ("Looks good. Good job!")

#step 3, check missing values infos
class CheckMissingValues(HelperBase):
    _var = 'missing_values_count'
    _solution = """
# Remplir la ligne ci-dessous: Combien de lignes sont dans les données d'entrainement?
num_rows = 1168

# Combien de colonnes dans les données d'entrainement ont des valeurs manquantes?
num_cols_with_missing = 3

# Combien d'entrées manquantes sont contenues dans toutes les données d'entrainement?
tot_missing = 212 + 6 + 58
"""
    _hint = """
Voir les infos dans missing_val_count_by_column ci-dessus
"""

    def check(self, num_rows, num_cols_with_missing, tot_missing):
        if num_rows != 1168:
            print_code_with_colors ("Expected num_rows to be 1168, but got {}".format(num_rows))
            return
        if num_cols_with_missing != 3:
            print_code_with_colors ("Expected num_cols_with_missing to be 3, but got {}".format(num_cols_with_missing))
            return
        if tot_missing != 276:
            print_code_with_colors ("Expected tot_missing to be 276, but got {}".format(tot_missing))
            return
        
        print_code_with_colors ("Looks good. Good job!")

# step 4, check the code to drop columns with missing values
class CheckDropColumns(HelperBase):
    _var = 'reduced_X_train'
    _solution = """
# Remplir la ligne ci-dessous: obtenir les noms des colonnes avec des valeurs manquantes
cols_with_missing = [col for col in X_train.columns if X_train[col].isnull().any()]

# Remplir la ligne ci-dessous: supprimer les colonnes dans les données d'entrainement et de validation
X_train_reduced = X_train.drop(cols_with_missing, axis=1)
X_valid_reduced = X_valid.drop(cols_with_missing, axis=1)
"""
    _hint = """
Utiliser X_train[col].isnull().any() pour savoir si une colonne contient des valeurs manquantes
Utiliser drop pour supprimer les colonnes
"""
    score = 23842.062627904717
    def check(self, X_train_reduced, X_valid_reduced, score):
        if X_train_reduced.shape != (1168, 34):
            print_code_with_colors ("Expected X_train_reduced to have shape (1168, 34), but got {}".format(X_train_reduced.shape))
            return
        if X_valid_reduced.shape != (292, 34):
            print_code_with_colors ("Expected X_valid_reduced to have shape (292, 34), but got {}".format(X_valid_reduced.shape))
            return
        
        if score != self.score:
            print_code_with_colors (f"Expected score to be {self.score}, but got {score}")
            return

        print_code_with_colors ("Looks good. Good job!")

# step 5, supprimer des colonnes avec des valeurs manquantes
class CheckCatColumns(HelperBase):
    _var = 'reduced_X_train'
    _solution = """
# Pour simplifier, nous allons supprimer les colonnes avec des valeurs manquantes
cols_with_missing = [col for col in home_data.columns if home_data[col].isnull().any()] 
X = home_data.drop(cols_with_missing, axis=1)
X.drop(['SalePrice'], axis=1, inplace=True)

# Diviser les données en sous-ensembles d'entrainement et de validation
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2,
                                                      random_state=0)
"""
    _hint = """
# Utiliser home_data[col].isnull().any() pour savoir si une colonne contient des valeurs manquantes
# Utiliser drop pour supprimer les colonnes
"""

    def check(self, X_train, X_valid, y_train, y_valid):
        if X_train.shape != (1168, 61):
            print_code_with_colors ("Expected X_train to have shape (1168, 61), but got {}".format(X_train.shape))
            return
        if X_valid.shape != (292, 61):
            print_code_with_colors ("Expected X_valid to have shape (292, 61), but got {}".format(X_valid.shape))
            return
        if y_train.shape != (1168,):
            print_code_with_colors ("Expected y_train to have shape (1168,), but got {}".format(y_train.shape))
            return
        if y_valid.shape != (292,):
            print_code_with_colors ("Expected y_valid to have shape (292,), but got {}".format(y_valid.shape))
            return
        
        print_code_with_colors ("Looks good. Good job!")

# step 6 : drop categorical columns
class CheckDropCatColumns(HelperBase):
    _var = 'drop_X_train'
    _solution = """
# Remplissez les lignes ci-dessous : supprimez les colonnes dans les données d'entraînement et de validation
drop_X_train = X_train.select_dtypes(exclude=['object'])
drop_X_valid = X_valid.select_dtypes(exclude=['object'])
# Le code suivant fonctionne après avoir supprimé les variables catégorielles
score = score_dataset(drop_X_train, drop_X_valid, y_train, y_valid)
    """
    _hint = """
# Utiliser select_dtypes pour exclure les colonnes catégorielles : exclude=['object']
"""

    def check(self, drop_X_train, drop_X_valid, score):
        if drop_X_train.shape != (1168, 34):
            print_code_with_colors ("Expected drop_X_train to have shape (1168, 34), but got {}".format(drop_X_train.shape))
            return
        if drop_X_valid.shape != (292, 34):
            print_code_with_colors ("Expected drop_X_valid to have shape (292, 34), but got {}".format(drop_X_valid.shape))
            return
        if score != 23842.062627904717:
            print_code_with_colors ("Expected score to be 23842.062627904717, but got {}".format(score))
            return
        
        print_code_with_colors ("Looks good. Good job!")

# step 7 : check the cardinality of categorical columns
class CheckCardinality(HelperBase):
    _var = 'low_cardinality_cols'
    _solution = """
high_cardinality_numcols = 3
num_cols_neighborhood = 25
""" 
    _hint = """
# Utilisez la sortie ci-dessus pour répondre aux questions ci-dessous.
"""

    def check(self, high_cardinality_numcols, num_cols_neighborhood):
        if high_cardinality_numcols != 3:
            print_code_with_colors ("Expected high_cardinality_numcols to be 3, but got {}".format(high_cardinality_numcols))
            return
        if num_cols_neighborhood != 25:
            print_code_with_colors ("Expected num_cols_neighborhood to be 25, but got {}".format(num_cols_neighborhood))
            return
        
        print_code_with_colors ("Looks good. Good job!")

# Step 8: check the number of added entries after one-hot encoding
class CheckOneHot(HelperBase):
    _var = 'OH_cols_train'
    _solution = """
#  1e4*100 de nouvelles entrées et 1e4 anciennes entrées seront supprimées
OH_entries_added = 1e4*100 - 1e4
# 1e4 nouvelles entrées replacent 1e4 anciennes entrées 
label_entries_added = 0
"""
    _hint = """
# Avec 100 valeurs uniques et 10000 lignes, on aura des entrées supplémentaires pour 100 colonnes et 10000 lignes.
# Dans le cas de l'encodage ordinal, 100 valeurs uniques seront représentées par les valeurs 0 à 99, donc 1 colonne et 10000 lignes.
"""

    def check(self, OH_entries_added, label_entries_added):
        if OH_entries_added != 990000.0:
            print_code_with_colors ("Expected OH_entries_added to be 990000.0, but got {}".format(OH_entries_added))
            return
        if label_entries_added != 0:
            print_code_with_colors ("Expected label_entries_added to be 0, but got {}".format(label_entries_added))
            return
        
        print_code_with_colors ("Looks good. Good job!")

# step 9: l'encodage One-Hot. Trouver low_cardinality_cols et high_cardinality_cols
class CheckEncodage(HelperBase):
    _var = 'OH_X_train'
    _solution = """
# Colonnes qui seront encodées en one-hot
low_cardinality_cols = [col for col in object_cols if X_train[col].nunique() < 10]
# Colonnes qui seront supprimées du dataset
high_cardinality_cols = list(set(object_cols)-set(low_cardinality_cols))
    """
    _hint = """
# Utiliser X_train[col].nunique() < 10 pour trouver les colonnes avec un nombre de valeurs uniques inférieur à 10
"""

    def check(self, low_cardinality_cols, high_cardinality_cols):
        if low_cardinality_cols != ['MSZoning', 'Street', 'LotShape', 'LandContour', 'Utilities', 'LotConfig', 'LandSlope', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl', 'ExterQual', 'ExterCond', 'Foundation', 'Heating', 'HeatingQC', 'CentralAir', 'KitchenQual', 'Functional', 'PavedDrive', 'SaleType', 'SaleCondition']:
            print_code_with_colors ("Expected low_cardinality_cols to be ['MSZoning', 'Street', 'LotShape', 'LandContour', 'Utilities', 'LotConfig', 'LandSlope', 'Condition1', 'Condition2', 'BldgType', 'HouseStyle', 'RoofStyle', 'RoofMatl', 'ExterQual', 'ExterCond', 'Foundation', 'Heating', 'HeatingQC', 'CentralAir', 'KitchenQual', 'Functional', 'PavedDrive', 'SaleType', 'SaleCondition'], but got {}".format(low_cardinality_cols))
            return
        if high_cardinality_cols != ['Exterior2nd', 'Neighborhood', 'Exterior1st']:
            print_code_with_colors ("Expected high_cardinality_cols to be ['Exterior2nd', 'Neighborhood', 'Exterior1st'], but got {}".format(high_cardinality_cols))
            return

        print_code_with_colors ("Looks good. Good job!")

# Step 10: check results of one-hot encoding
class CheckResults(HelperBase):
    _var = 'OH_X_train'
    _solution = """
# Appliquer un encodeur one-hot à chaque colonne avec des données catégorielles
OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
OH_cols = pd.DataFrame(OH_encoder.fit_transform(X[low_cardinality_cols]))
# One-hot encodage supprime l'index; le remettre
OH_cols.index = X.index
# Supprimer les colonnes catégorielles (sera remplacé par l'encodage one-hot)
num_X = X.drop(object_cols, axis=1)
# Ajouter les colonnes encodées one-hot aux caractéristiques numériques
OH_X = pd.concat([num_X, OH_cols], axis=1)
# Assurer que toutes les colonnes sont des strings
OH_X.columns = OH_X.columns.astype(str)
OH_X_train, OH_X_valid, y_train, y_valid = train_test_split(OH_X, y, train_size=0.8, test_size=0.2,
                                                      random_state=0)
score = score_dataset(OH_X_train, OH_X_valid, y_train, y_valid)                                                      
                                                    """
    _hint = """
# Utiliser OneHotEncoder pour encoder les colonnes catégorielles
# Transformer les données catégorielles low_cardinality_cols
# Drop les colonnes catégorielles originales object_cols
# Utiliser pd.concat pour ajouter les colonnes encodées one-hot aux caractéristiques numériques
"""

    def check(self, OH_X_train, OH_X_valid, y_train, y_valid, score ):  
        if score != 24532.98600376439:
            print_code_with_colors ("Expected score to be 24532.98600376439, but got {}".format(score))
            return
        
        print_code_with_colors ("Great job!")


step1 = CheckScoreDataset()    
step2 = CheckAllColumns()  
step3 = CheckMissingValues()
step4 = CheckDropColumns()
step5 = CheckCatColumns()
step6 = CheckDropCatColumns()
step7 = CheckCardinality()
step8 = CheckOneHot()
step9 = CheckEncodage()
step10 = CheckResults()