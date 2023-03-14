from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class PopupWindow(QMainWindow):
    """Class generates popup windows used for warnings and error messages."""
    def __init__(self, source, title_message, subtitle_message, body_message):
        super().__init__()
        self.source = source

        self.setGeometry(100, 150, 300, 200)
        self.setWindowTitle(title_message)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(40)

        subtitle_label = QLabel(subtitle_message)
        subtitle_label.setFont(QFont('Arial', 11))
        subtitle_label.setAlignment(Qt.AlignCenter)

        body_label = QLabel(body_message)
        body_label.setAlignment(Qt.AlignCenter)

        button_hold = QHBoxLayout()
        button_hold.setAlignment(Qt.AlignCenter)

        self.okay_button = QPushButton("Okay")
        self.okay_button.setFixedWidth(50)
        self.okay_button.clicked.connect(self.okay_button_pushed)
        button_hold.addWidget(self.okay_button)

        layout.addWidget(subtitle_label)
        layout.addWidget(body_label)
        layout.addLayout(button_hold)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def okay_button_pushed(self):
        self.close()
        self.source.show()

