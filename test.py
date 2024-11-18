from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, QPushButton
from PyQt5.QtCore import Qt

class HUDApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Seleção de Matéria")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: #00247c; color: white;")

        title_label = QLabel("SELECIONE A MATÉRIA:")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.subject_combo = QComboBox()
        self.subject_combo.addItems(["POO", "AOC", "EDD", "CALC2", "LFA"])
        self.subject_combo.setStyleSheet("background-color: white; color: black; padding: 5px;")

        professor_label = QLabel("PROFESSOR(A):")
        professor_label.setAlignment(Qt.AlignCenter)
        professor_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.professor_input = QLineEdit()
        self.professor_input.setStyleSheet("background-color: white; color: black; padding: 5px;")

        confirm_button = QPushButton("CONFIRMAR")
        confirm_button.setStyleSheet("background-color: black; color: white; font-size: 14px; font-weight: bold; padding: 10px;")

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.subject_combo)
        layout.addWidget(professor_label)
        layout.addWidget(self.professor_input)
        layout.addWidget(confirm_button)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    hud_app = HUDApp()
    hud_app.show()
    sys.exit(app.exec_())
