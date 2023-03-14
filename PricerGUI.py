from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit,\
    QPushButton
from PyQt5.QtGui import QPixmap
import numpy as np
import DiamondModel
import LoginGUI
import AdminGUI
import PopupGUI
from datetime import datetime


class DropDown:
    """Class for labeled combobox"""
    def __init__(self, label, items):
        self.holder = QHBoxLayout()
        self.label = QLabel(label)
        self.box = QComboBox()
        self.box.addItems(items)

        self.holder.addWidget(self.label)
        self.holder.addWidget(self.box)


class PricerWindow(QMainWindow):

    def __init__(self, admin_flag, prediction_model):
        super().__init__()

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Pricing')

        layout = QVBoxLayout()

        # Store values
        self.carat = 0.0
        self.cut = 0
        self.clarity = 0
        self.color = 0

        # Create top label
        label_holder = QHBoxLayout()
        instructions_label = QLabel("Enter carat and select characteristics, then click 'Go'")
        label_holder.addWidget(instructions_label)
        layout.addLayout(label_holder)

        # Create Lower area
        inout_hbox = QHBoxLayout()

        # Create input area
        in_vbox = QVBoxLayout()
        v_widget = QWidget()
        v_widget.setLayout(in_vbox)
        v_widget.setFixedWidth(250)

        carat_row = QHBoxLayout()
        carat_label = QLabel("Carats:")
        self.carat_line = QLineEdit()
        carat_row.addWidget(carat_label)
        carat_row.addWidget(self.carat_line)
        in_vbox.addLayout(carat_row)

        self.cut_row = DropDown('Cut', DiamondModel.CUT_MAPPING.keys())
        in_vbox.addLayout(self.cut_row.holder)
        self.cut_row.box.currentTextChanged.connect(self.cut_selection_changed)

        self.clarity_row = DropDown('Clarity', DiamondModel.CLARITY_MAPPING.keys())
        in_vbox.addLayout(self.clarity_row.holder)
        self.clarity_row.box.currentTextChanged.connect(self.clarity_selection_changed)

        self.color_row = DropDown('Color', DiamondModel.COLOR_MAPPING.keys())
        in_vbox.addLayout(self.color_row.holder)
        self.color_row.box.currentTextChanged.connect(self.color_selection_changed)

        inout_hbox.addWidget(v_widget)

        # Create output area
        out_vbox = QVBoxLayout()

        self.graph_label = QLabel()
        self.graph_image = QPixmap()
        self.graph_label.setPixmap(self.graph_image)
        out_vbox.addWidget(self.graph_label)

        self.price_readout = QLabel("Price: $0.00 +- 0.00")
        self.price_readout.setStyleSheet("border: 1px solid black")
        self.price_readout.setFixedWidth(250)
        self.price_readout.setFixedHeight(50)
        out_vbox.addWidget(self.price_readout)

        inout_hbox.addLayout(out_vbox)
        layout.addLayout(inout_hbox)

        # Create lower area
        calculate_button = QPushButton("Calculate Price")
        calculate_button.clicked.connect(self.calculate_button_pushed)

        logout_button = QPushButton("Log Out")
        logout_button.clicked.connect(self.logout_button_pushed)

        admin_button = QPushButton("Model Control")
        admin_button.clicked.connect(self.admin_button_pushed)

        # If user is admin, include button to access admin window. Otherwise, do not
        if admin_flag:
            lower_hbox = QHBoxLayout()
            lower_hbox.addWidget(calculate_button)
            lower_hbox.addWidget(logout_button)
            lower_hbox.addWidget(admin_button)
            layout.addLayout(lower_hbox)

        else:
            lower_vbox = QVBoxLayout()
            lower_vbox.addWidget(calculate_button)
            lower_vbox.addWidget(logout_button)
            layout.addLayout(lower_vbox)

        # Complete creation
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Save model
        self.model = prediction_model

        # Empty attributes to store handles for other windows
        self.login = None
        self.popup = None
        self.admin = None

    def admin_button_pushed(self):
        """Slot to catch admin button click. Opens admin window"""
        # print("Admin button was pushed")
        self.admin = AdminGUI.AdminWindow(self.model)
        self.admin.show()
        self.close()

    def calculate_button_pushed(self):
        """Slot to catch calculate button click. Validate carat entry and calculate price"""
        print("The calculate button was pushed")

        try:
            self.carat = float(self.carat_line.text())

            if self.carat > 0:  # Carat value must be a positive number
                x_input = np.array([[self.carat, float(self.cut), float(self.color), float(self.clarity)]])
                prediction = self.model.make_prediction(x_input)
                # print("DEBUG: make_prediction returns")
                # print("Predicted value is {:.2f} plus or minus {:.2f}".format(prediction,
                                                                              # self.model.prediction_interval))
                self.price_readout.setText("${:.2f} +- ${:.2f}".format(prediction, self.model.prediction_interval))

                self.model.prediction_chart(prediction)
                self.graph_image.load('barchart.png')
                self.graph_label.setPixmap(self.graph_image)
            else:
                print("Carat below 0")

                self.popup = PopupGUI.PopupWindow(self,
                                                  "BAD ENTRY",
                                                  "Invalid Carat",
                                                  "Carat value must be greater than zero")
                self.hide()
                self.popup.show()

                with open('bad_carat_record.txt', 'a') as file:
                    file.write("\"{}\",{}\n".format(self.carat_line.text(), datetime.now()))
                self.carat_line.clear()

        # Catch invalid entries in carat field
        except ValueError:
            print("Bad carat value")

            self.popup = PopupGUI.PopupWindow(self,
                                              "BAD ENTRY",
                                              "Invalid Carat",
                                              "Carat value must be numeric")
            self.hide()
            self.popup.show()

            with open('bad_carat_record.txt', 'a') as file:
                file.write("\"{}\",{}\n".format(self.carat_line.text(), datetime.now()))
            self.carat_line.clear()

    def cut_selection_changed(self):
        """Slot to catch change in cut selection. Update cut attribute"""
        self.cut = DiamondModel.CUT_MAPPING[self.cut_row.box.currentText()]
        # DEBUG print("Cut is {}".format(self.cut))

    def clarity_selection_changed(self):
        """Slot to catch change in clarity selection. Update clarity attribute"""
        self.clarity = DiamondModel.CLARITY_MAPPING[self.clarity_row.box.currentText()]
        # DEBUG print("Clarity is {}".format(self.clarity))

    def color_selection_changed(self):
        """Slot to catch change in color selection. Update color attribute"""
        self.color = DiamondModel.COLOR_MAPPING[self.color_row.box.currentText()]
        # DEBUG print("Color is {}".format(self.color))

    def logout_button_pushed(self):
        """Slot to catch logout button click. Return to login window"""
        # print("Log out button was pushed")
        self.login = LoginGUI.LoginWindow(self.model)
        self.login.show()
        self.close()

