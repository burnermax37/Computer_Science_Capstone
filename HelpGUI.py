from PyQt5.QtWidgets import QMainWindow, QLabel,\
    QVBoxLayout, QWidget, QPushButton, QHBoxLayout


class HelpWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        r_squared_help_text = "R-Squared: The value should be as close as possible to 1.0. A value below 0.9 \n" \
                        "indicates the model is not sufficiently accurate, and needs to be revised."

        resid_help_text = "Residuals Fit Plot: The plotted points should form a fuzzy rectangle whose midline\n" \
                        "lays on the x-axis (y = 0). Significant variation in the vertical thickness of the\n" \
                        "point cloud indicates uneven distribution of residuals. More important, the red line\n" \
                        "should lay flat on the x-axis: if it has a notable slope or curve, there are trends in \n" \
                        "the residuals, indicating relationships between price and predictors not caught by the\n"\
                        "predictive model."

        qq_help_text = "QQ-Normality Plot: The colored line formed by the plotted points should mostly lay flat\n" \
                        "against the dashed line. Significant divergence across the whole width of the plot means\n" \
                        "that model residuals do not follow a normal distribution, indicating a possible issue."

        r_squared_help_label = QLabel(r_squared_help_text)
        resid_help_label = QLabel(resid_help_text)
        qq_help_label = QLabel(qq_help_text)

        layout.addWidget(r_squared_help_label)
        layout.addWidget(resid_help_label)
        layout.addWidget(qq_help_label)

        # Back area
        button_hbox = QHBoxLayout()
        close_button = QPushButton("Close")
        close_button.setFixedWidth(200)
        close_button.clicked.connect(self.close_button_pushed)

        button_hbox.addWidget(close_button)
        layout.addLayout(button_hbox)

        # Finalize
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def close_button_pushed(self):
        """Receiver slot for pushing back button. Close help popup window"""
        print("Close button was pushed")
        self.close()
