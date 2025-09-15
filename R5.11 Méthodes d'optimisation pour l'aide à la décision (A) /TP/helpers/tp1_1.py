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

class LoadHomeData(HelperBase):
    _var = 'home_data'
    _hint = "# Use the `pd.read_csv` function"
    _solution = 'home_data = pd.read_csv(iowa_file_path)'
    # # make _solution colorful to show in mardown notebook without using CS
    # # _solution = "<font color='red'>Solution:</font> {}".format(_solution)

    def check(self, df):

        if not isinstance(df, pd.DataFrame):
            print_code_with_colors ("home_data should be a DataFrame,"
                " not {}".format(type(df)))
            return
        
        expected_shape = (1460, 81)
        if df.shape != expected_shape:
            print_code_with_colors ("Expected {} rows and {} columns, but"
                " got shape {}".format(expected_shape[0], expected_shape[1], df.shape))
            return

        print_code_with_colors ("home_data looks good. Good job!")

class HomeDescription(HelperBase):
    _vars = ['avg_lot_size', 'newest_home_age']
    max_year_built = 2010
    min_home_age = datetime.datetime.now().year - max_year_built
    _expected = [10517, min_home_age]
    _hint = '# Run the describe command. Lot size is in the column called LotArea. Also look at YearBuilt. Remember to round lot size '
    _solution = """# using data read from home_data.describe()
avg_lot_size = 10517
newest_home_age = {}
""".format(min_home_age)
    
    def check(self, avg_lot_size, newest_home_age):
        assert_with_color(avg_lot_size == self._expected[0], "avg_lot_size should be {}".format(self._expected[0]))
        assert_with_color(newest_home_age == self._expected[1], "newest_home_age should be {}".format(self._expected[1]))

        # print_code_with_colors("Good job! That's right.")

# class for step 3, verifier la variable cible 
class TargetVariable(HelperBase):
    _var = 'y'
    _hint = '# SalePrice '
    _solution = "y = home_data.SalePrice"
    expected_shape = (1460,)
    expected_name = 'SalePrice'

    def check(self, df):
        if df.shape != (1460,) or df.name != self.expected_name:
            print_code_with_colors (f"Expected column {self.expected_name} and shape {self.expected_shape}, but"
                f" got name {df.name} shape {df.shape}")
            return
        print_code_with_colors("Good job! That's right.")


# step 4, load data from list of features
class LoadDataFromList(HelperBase):
    _var = 'features'
    _hint = """
# Create a list of features called `feature_names` then load the data to X from home_data. 
# X = home_data[feature_names]"""
    _solution = """
feature_names = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']
X = home_data[feature_names]"""

    def check(self, df, feature_names):
        if df.columns.tolist() != feature_names:
            print_code_with_colors (f"Expected column names {feature_names}, but"
                f" got {df.name}")
            return
        print_code_with_colors("Good job! That's right.")

class SplitData(HelperBase):
    _var = 'train_X'
    _hint = """
# Use the `train_test_split` function to split up your data.
# Give it the argument `random_state=1` so the `check` functions know what to expect when verifying your code.
# Recall, your features are loaded in the DataFrame named `X` and your target is loaded in `y`.
# The functions `train_test_split` and `train_test_split` will do the rest.
# """
    _solution = """
from sklearn.model_selection import train_test_split
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)"""

    def check(self, train_X, val_X, train_y, val_y):
        if train_X.shape != (1095, 7):
            print_code_with_colors (f"Expected train_X shape (1095, 7), but"
                f" got {train_X.shape}")
            return
        if val_X.shape != (365, 7):
            print_code_with_colors (f"Expected val_X shape (365, 7), but"
                f" got {val_X.shape}")
            return
        if train_y.shape != (1095,):
            print_code_with_colors (f"Expected train_y shape (1095,), but"
                f" got {train_y.shape}")
            return
        if val_y.shape != (365,):
            print_code_with_colors (f"Expected val_y shape (365,), but"
                f" got {val_y.shape}")
            return
        print_code_with_colors("Good job! That's right.")

#Check the fitted model 
from sklearn.linear_model import LinearRegression
class CheckModel(HelperBase):
    _var = 'iowa_model'
    _hint = """
# Define a LinearRegression model. 
# Fit the model with the training data in `train_X` and the training target data in `train_y`"""
    _solution = """
from sklearn.linear_model import LinearRegression
iowa_model = LinearRegression()
iowa_model.fit(train_X, train_y)"""

    def check(self, iowa_model):
        if not isinstance(iowa_model, LinearRegression):
            print_code_with_colors ("iowa_model should be a LinearRegression,"
                " not {}".format(type(iowa_model)))
            return
        print_code_with_colors("Good job! That's right.")

# step7, verification du modele on val data
class CheckModelOnValData(HelperBase):
    _var = 'val_predictions'
    _hint = """
# Predict with all validation observations
val_predictions = iowa_model.predict(val_X)"""
    _solution = """
val_predictions = iowa_model.predict(val_X)"""

    def check(self, val_predictions):
        if val_predictions.shape != (365,):
            print_code_with_colors (f"Expected val_predictions shape (365,), but"
                f" got {val_predictions.shape}")
            return
        print_code_with_colors("Good job! That's right.")

#step 8, calcul de l'erreur de prediction par mean_absolute_error et ecrire la fonction de calcul de l'erreur
# ensuite comparer les 2 erreurs
class CheckMAE(HelperBase):
    _var = 'val_mae'
    _hint = """
# Use the `mean_absolute_error` function to calculate the mean absolute error (MAE) between `val_y` and `val_predictions`
# Write your function :
# def mae(y_true, y_pred):
#     return ___"""
    _solution = """
from sklearn.metrics import mean_absolute_error
val_mae = mean_absolute_error(val_y, val_predictions)
def mae(y_true, y_pred):
    return sum(abs(y_true - y_pred)) / len(y_true)
"""
    def check(self, val_mae, mae):
        if val_mae != mae:
            print_code_with_colors (f"Expected val_mae {mae}, but"
                f" got {val_mae}")
            print_code_with_colors (f"But it is ok if the difference is very small")
            return

step1 = LoadHomeData()
step2 = HomeDescription()
step3 = TargetVariable()
step4 = LoadDataFromList()
step5 = SplitData()
step6 = CheckModel()
step7 = CheckModelOnValData()
step8 = CheckMAE()