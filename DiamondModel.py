import numpy as np
from sklearn.model_selection import KFold
import pandas as pd
import joblib
from matplotlib import pyplot as plt

CUT_MAPPING = {'Fair': 0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4}
COLOR_MAPPING = {'D': 0, 'E': 1, 'F': 2, 'G': 3, 'H': 4, 'I': 5, 'J': 6}
CLARITY_MAPPING = {'I1': 0, 'SI2': 1, 'SI1': 2, 'VS2': 3, 'VS1': 4, 'VVS2': 5, 'VVS1': 6, 'IF': 7}


class DiamondPredictor:
    """Class instance stores methods and parameters to create and use model"""
    def __init__(self, new_model, model):
        # print("DEBUG: Init runs")
        self.prediction_interval = None
        self.model_stack = None
        self.r_2 = None
        self.training_n = None

        if new_model:
            print("Making new model")
            # If model needs to be remade, call make_model
            self.make_model(model)

        else:
            print("Loading existing model")
            self.loadmodel()

    @staticmethod
    def process_training_data(in_data):
        """Process raw data for modeling"""
        # print("DEBUG: Process_training data_runs")
        x_out = np.column_stack((
            in_data['carat'],
            in_data['cut'].map(CUT_MAPPING),
            in_data['color'].map(COLOR_MAPPING),
            in_data['clarity'].map(CLARITY_MAPPING)
        ))

        y_out = np.array(in_data['price'])

        return x_out, y_out

    @staticmethod
    def crossval_plus(model, x_tr, y_tr, folds=20):
        """Method to generate confidence interval and stack of models for predictions"""
        # print("DEBUG: crossval_plus runs")
        kf = KFold(n_splits=folds, shuffle=True, random_state=42)
        estimators = []
        residuals = []

        alpha = 0.05

        # Use remove-one models to get residuals, while saving each model
        for train_idx, test_idx in kf.split(x_tr):
            x_train_, x_test__ = x_tr[train_idx], x_tr[test_idx]
            y_train_, y_test_ = y_tr[train_idx], y_tr[test_idx]

            # Fit model, and copy to estimators stack
            model.fit(x_train_, y_train_)
            estimators.append(model)

            prediction = model.predict(x_test__)
            residuals.extend(y_test_ - prediction)

        # Calculate confidence intervals
        pred_interval = np.quantile(np.array(residuals), 1 - alpha)

        return pred_interval, estimators

    @staticmethod
    def r_squared(observed, predicted):
        """Calculate R-squared based on observed versus expected values"""
        observed_mean = observed.mean()
        total_sum_squares = sum([(observed[i] - observed_mean) ** 2 for i in range(len(observed))])
        sum_squared_regression = sum([(observed[i] - predicted[i]) ** 2 for i in range(len(observed))])
        return 1 - (sum_squared_regression / total_sum_squares)

    def prediction_chart(self, predicted_value):
        """Create bar chart showing predicted price of diamond compared to mean and median"""
        # print("DEBUG: prediction_chart runs")
        raw_data = pd.read_csv(r'diamonds.csv')
        raw_data = raw_data[(raw_data['x'] > 0) & (raw_data['y'] > 0) & (raw_data['z'] > 0)]
        mean = raw_data[['price']].mean()[0]
        med = raw_data[['price']].median()[0]

        fig, ax = plt.subplots()
        ax.bar([-1, 0, 1], [predicted_value, mean, med], yerr=[self.prediction_interval, 0, 0], width=[0.4], alpha=0.5, ecolor='black',
               capsize=10)
        ax.set_ylabel("Predicted Price")
        ax.set_xticks([-1, 0, 1])
        ax.set_xticklabels(['Predicted\nDiamond Price', 'Mean Diamond Price', 'Median Diamond Price'])
        ax.set_title('Predicted Price of Your Diamond')
        plt.savefig("barchart.png")
        plt.clf()

    def model_diagnostic_charts(self, y_train, x_train):
        """Create diagnostic plots of model"""
        # print("DEBUG: make_charts runs")
        training_predictions = []

        for i in range(len(y_train)):
            training_predictions.append(self.make_prediction([x_train[i]]))

        r_2 = DiamondPredictor.r_squared(y_train, training_predictions)

        training_residuals = y_train - training_predictions
        training_residuals_standard = (training_residuals - training_residuals.mean()) / training_residuals.std()

        # Create plot of residuals versus fitted values

        plt.scatter(training_predictions, training_residuals, alpha=0.1)

        lin_x = np.linspace(plt.xlim()[0], plt.xlim()[1], 100)
        lin_y = np.zeros(100)
        a, b = np.polyfit(training_predictions, training_residuals, 1)

        for item in np.polyfit(training_predictions, training_residuals, 1):
            print(item)

        plt.plot(lin_x, lin_y, color='k', ls="--")
        plt.plot(training_predictions, a * np.array(training_predictions) + b, color='red')

        plt.xlabel("Predicted Values")
        plt.ylabel("Residuals")
        plt.title("Residuals versus Fitted Values")
        plt.savefig("resid_fit_plt.png")
        plt.clf()

        # Create plot QQ plot comparing residuals to normal distribution
        theoretical = np.random.normal(0, 1, 100)

        percs = np.linspace(0, 100, len(training_residuals_standard))
        qn_residuals = np.percentile(training_residuals_standard, percs)
        qn_theoretical = np.percentile(theoretical, percs)
        lin = np.linspace(np.min((qn_theoretical.min(), qn_residuals.min())),
                          np.max((qn_theoretical.max(), qn_residuals.max())))

        plt.plot(qn_theoretical, qn_residuals, ls="", marker='o', alpha=0.05)
        plt.xlabel("Theoretical Quantiles")
        plt.ylabel("Observed Quantiles")
        plt.xlim(np.min(qn_theoretical) * 1.2, np.max(qn_theoretical) * 1.2)
        plt.ylim(np.min(qn_residuals) * 1.2, np.max(qn_residuals) * 1.2)
        plt.title("QQ Normality Plot")
        plt.plot(lin, lin, color='k', ls="--")
        plt.savefig("qq_normality.png")
        plt.clf()

        return r_2

    def make_model(self, model):
        """Use data to create predictive model, save model and side data to file"""
        # print("DEBUG: make_model runs")

        # Load and process data, saving size of training data
        raw_data = pd.read_csv(r'diamonds.csv')
        raw_data = raw_data[(raw_data['x'] > 0) & (raw_data['y'] > 0) & (raw_data['z'] > 0)]

        x_train, y_train = DiamondPredictor.process_training_data(raw_data)

        # Calculate and save models and prediction interval
        self.prediction_interval, self.model_stack = DiamondPredictor.crossval_plus(model, x_train, y_train)

        self.r_2 = self.model_diagnostic_charts(y_train, x_train)
        self.training_n = len(y_train)

        file_dict = dict({
            "Prediction Interval": self.prediction_interval,
            "Model Stack": self.model_stack,
            "R-squared": self.r_2,
            "Training Size": len(y_train)
        })

        joblib.dump(file_dict, 'dict_file.joblib')

    def loadmodel(self):
        # Load existing model from joblib file
        model_dict = joblib.load('dict_file.joblib')
        self.prediction_interval = model_dict['Prediction Interval']
        self.model_stack = model_dict['Model Stack']
        self.r_2 = model_dict['R-squared']
        self.training_n = model_dict['Training Size']

    def make_prediction(self, x_tst):
        """Make prediction with each saved model, get median prediction"""
        # print("DEBUG: make_prediction runs")
        y_pred_multi = np.column_stack([e.predict(x_tst) for e in self.model_stack])
        preds = np.median(y_pred_multi, axis=1)
        return preds[0]
