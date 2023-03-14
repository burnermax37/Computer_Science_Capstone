from PyQt5.QtWidgets import QApplication

import LoginGUI
import DiamondModel
from sklearn import tree
import sys
from os import path
import numpy as np


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Check if joblib file storing model data exists
    model_exists = path.exists('dict_file.joblib')
    if model_exists:
        print("joblib file exists")

    # Load existing model if one is present, otherwise create new model
    model = DiamondModel.DiamondPredictor(not model_exists, tree.DecisionTreeRegressor())

    # Start Qt application
    app = QApplication(sys.argv)
    window = LoginGUI.LoginWindow(model)
    window.show()
    sys.exit(app.exec_())


