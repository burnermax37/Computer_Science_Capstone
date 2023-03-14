from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QPixmap
from sklearn.tree import DecisionTreeRegressor
import DiamondModel
import PricerGUI
import HelpGUI


class AdminWindow(QMainWindow):
    def __init__(self, predictive_model):
        super().__init__()

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Admin Tools')

        layout = QVBoxLayout()

        self.model = predictive_model

        # Text Info Area
        text_vbox = QVBoxLayout()
        text_vbox.setContentsMargins(40, 10, 30, 10)

        # Label displaying R-squared value and number of training observations
        self.parameter_label = QLabel("Model R-squared: {:.2f} \n\nNo of Training Observations: {}".format(
            self.model.r_2,
            self.model.training_n
        ))
        self.parameter_label.setFixedWidth(300)
        self.parameter_label.setStyleSheet("border: 1px solid black")

        text_vbox.addWidget(self.parameter_label)
        layout.addLayout(text_vbox)

        # Image Area
        image_hbox = QHBoxLayout()

        self.residuals_fitted_label = QLabel()
        self.residuals_fitted_image = QPixmap("resid_fit_plt.png")
        self.residuals_fitted_label.setPixmap(self.residuals_fitted_image)
        image_hbox.addWidget(self.residuals_fitted_label)

        self.qq_label = QLabel()
        self.qq_image = QPixmap("qq_normality.png")
        self.qq_label.setPixmap(self.qq_image)
        image_hbox.addWidget(self.qq_label)

        layout.addLayout(image_hbox)

        # Upper Button Area
        upper_button_hbox = QHBoxLayout()
        self.help_button = QPushButton("Help")
        self.help_button.setFixedWidth(200)
        self.help_button.clicked.connect(self.help_button_pushed)
        upper_button_hbox.addWidget(self.help_button)

        self.update_button = QPushButton("Update Model")
        self.update_button.setFixedWidth(200)
        self.update_button.clicked.connect(self.update_button_pushed)
        upper_button_hbox.addWidget(self.update_button)

        layout.addLayout(upper_button_hbox)

        # Lower Button Area
        lower_button_hbox = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.back_button.setFixedWidth(100)
        self.back_button.clicked.connect(self.back_button_pushed)
        lower_button_hbox.addWidget(self.back_button)

        layout.addLayout(lower_button_hbox)

        # Finalize
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Empty attributes to hold handles for other windows
        self.pricer = None
        self.help_window = None

    def help_button_pushed(self):
        """Slot to catch help button click. Open help window."""
        # print("Help button was pushed")
        self.help_window = HelpGUI.HelpWindow()
        self.help_window.show()

    def update_button_pushed(self):
        """Slot to catch update button click. Create and save new model, update visuals."""
        # print("Update button was pushed")

        self.model = DiamondModel.DiamondPredictor(True, DecisionTreeRegressor())

        self.residuals_fitted_image.load('resid_fit_plt.png')
        self.residuals_fitted_label.setPixmap(self.residuals_fitted_image)

        self.qq_image.load('qq_normality.png')
        self.qq_label.setPixmap(self.qq_image)

    def back_button_pushed(self):
        """Slot to catch back button click. Return to prediction window."""
        # print("Back Button was Pushed")
        self.pricer = PricerGUI.PricerWindow(True, self.model)
        self.pricer.show()
        self.close()
