import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel, QHBoxLayout, QFormLayout
import psycopg2
from home import Home


class UserManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PostgreSQL User Management")
        self.setGeometry(100, 100, 400, 300)

        self.connection = None
        self.connect_to_db()

        self.initUI()

    def connect_to_db(self):
        try:
            self.connection = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="password",
                host="192.168.32.1",
                port="5432"
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT version();")
            db_version = self.cursor.fetchone()
            print(f"Connected to PostgreSQL database: {db_version}")
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error while connecting to PostgreSQL: {error}")
            self.connection = None

    def initUI(self):
        self.home = Home()
        self.setCentralWidget(self.home)
        # self.table_widget = QTableWidget()
        # self.status_label = QLabel("")
        # self.load_users()

        # self.add_button = QPushButton("Add User")
        # self.add_button.clicked.connect(self.add_user)
        # self.add_button.setToolTip("Click to add a new user with the specified username and password")

        # self.delete_button = QPushButton("Delete User")
        # self.delete_button.clicked.connect(self.delete_user)
        # self.delete_button.setToolTip("Select a user from the table and click to delete")

        # self.username_input = QLineEdit()
        # self.username_input.setPlaceholderText("Enter username")
        # self.username_input.setToolTip("Enter the username for the new user")

        # self.password_input = QLineEdit()
        # self.password_input.setEchoMode(QLineEdit.Password)
        # self.password_input.setPlaceholderText("Enter password")
        # self.password_input.setToolTip("Enter the password for the new user")

        # form_layout = QFormLayout()
        # form_layout.addRow("Username:", self.username_input)
        # form_layout.addRow("Password:", self.password_input)

        # button_layout = QHBoxLayout()
        # button_layout.addWidget(self.add_button)
        # button_layout.addWidget(self.delete_button)

        # main_layout = QVBoxLayout()
        # main_layout.addWidget(QLabel("PostgreSQL User Management"))
        # main_layout.addWidget(self.table_widget)
        # main_layout.addLayout(form_layout)
        # main_layout.addLayout(button_layout)
        # main_layout.addWidget(self.status_label)

        # container = QWidget()
        # container.setLayout(main_layout)
        # self.setCentralWidget(container)

    def load_users(self):
        if self.connection:
            self.cursor.execute("SELECT usename FROM pg_user;")
            users = self.cursor.fetchall()
            self.table_widget.setRowCount(len(users))
            self.table_widget.setColumnCount(1)
            self.table_widget.setHorizontalHeaderLabels(["Username"])

            for row_index, user in enumerate(users):
                self.table_widget.setItem(row_index, 0, QTableWidgetItem(user[0]))
            self.status_label.setText(f"Loaded {len(users)} users.")
        else:
            self.status_label.setText("Failed to load users. No database connection.")

    def add_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            try:
                self.cursor.execute(f"CREATE USER {username} WITH PASSWORD '{password}';")
                self.connection.commit()
                self.load_users()
                QMessageBox.information(self, "Success", "User added successfully.")
                self.status_label.setText(f"User '{username}' added successfully.")
                self.username_input.clear()
                self.password_input.clear()
            except (Exception, psycopg2.DatabaseError) as error:
                QMessageBox.critical(self, "Error", str(error))
                self.status_label.setText(f"Error adding user '{username}'.")
        else:
            QMessageBox.warning(self, "Warning", "Please enter both username and password.")
            self.status_label.setText("Failed to add user. Username or password missing.")

    def delete_user(self):
        selected_items = self.table_widget.selectedItems()
        if selected_items:
            username = selected_items[0].text()
            try:
                self.cursor.execute(f"DROP USER {username};")
                self.connection.commit()
                self.load_users()
                QMessageBox.information(self, "Success", "User deleted successfully.")
                self.status_label.setText(f"User '{username}' deleted successfully.")
            except (Exception, psycopg2.DatabaseError) as error:
                QMessageBox.critical(self, "Error", str(error))
                self.status_label.setText(f"Error deleting user '{username}'.")
        else:
            QMessageBox.warning(self, "Warning", "Please select a user to delete.")
            self.status_label.setText("Failed to delete user. No user selected.")

    def closeEvent(self, event):
        if self.connection:
            self.cursor.close()
            self.connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserManagementApp()
    window.show()
    sys.exit(app.exec_())
