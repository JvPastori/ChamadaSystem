from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, QPushButton
from PyQt5.QtCore import Qt

class HUDApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Seleção de Matéria")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: ##f6eee0; color: white;")

        title_label = QLabel("SELECIONE A MATÉRIA:")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # ComboBox de Matérias
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(["POO", "AOC", "EDD", "CALC2", "LFA", "TDG"])
        self.subject_combo.setStyleSheet("background-color: white; color: black; padding: 5px;")
        self.subject_combo.currentTextChanged.connect(self.update_professors)

        professor_label = QLabel("PROFESSOR(A):")
        professor_label.setAlignment(Qt.AlignCenter)
        professor_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # ComboBox de Professores
        self.professor_combo = QComboBox()
        self.professor_combo.setStyleSheet("background-color: white; color: black; padding: 5px;")

        confirm_button = QPushButton("CONFIRMAR")
        confirm_button.setStyleSheet("background-color: black; color: white; font-size: 14px; font-weight: bold; padding: 10px;")

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.subject_combo)
        layout.addWidget(professor_label)
        layout.addWidget(self.professor_combo)
        layout.addWidget(confirm_button)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

        # Inicializa os professores
        self.professors_by_subject = {
            "POO": ["Corgosinho"],
            "AOC": ["Paulo"],
            "EDD": ["Kleber"],
            "CALC2": ["Luciana"],
            "LFA": ["Paulo"],
            "TDG": ["Jose Luis"]
        }
        self.update_professors(self.subject_combo.currentText())

    def update_professors(self, subject):
        """Atualiza os professores com base na matéria selecionada."""
        self.professor_combo.clear()
        if subject in self.professors_by_subject:
            self.professor_combo.addItems(self.professors_by_subject[subject])

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    hud_app = HUDApp()
    hud_app.show()
    sys.exit(app.exec_())
