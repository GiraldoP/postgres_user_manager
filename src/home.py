from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget

class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        # button_labels = ['Role Management', 'User Management', 'Change Connection']
        self.role_management_button = QPushButton('Role Management')
        self.user_management_button = QPushButton('User Management')
        self.change_connection_button = QPushButton('Change Connection')
        self.layout.addWidget(self.role_management_button)
        self.layout.addWidget(self.user_management_button)
        self.layout.addWidget(self.change_connection_button)
        self.setLayout(self.layout)