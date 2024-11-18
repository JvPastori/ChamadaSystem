from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class HUDApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()  # Inicializa a interface do usuário

    def init_ui(self):
        # Configurações da janela principal
        self.setWindowTitle("Seleção de Matéria")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f6eee0, 
                    stop:1 #8e9eab
                ); 
                color: white;
            }
        """)

        # Imagem no topo
        image_label = QLabel()
        pixmap = QPixmap("C:\\Users\\gk\\Downloads\\facul\\ChamadaSystem\\unespar.png")  
        if not pixmap.isNull():
            pixmap = pixmap.scaled(300, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # Título da seleção de matéria
        title_label = QLabel("SELECIONE A MATÉRIA:")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # ComboBox de Matérias
        self.subject_combo = QComboBox()
        self.subject_combo.addItems([
            "Pogramação Orientada a Objetos", 
            "Arquitetura e Organização de Computadores", 
            "Estrutura de Dados", 
            "Cálculo II", 
            "Linguagens Formais e Autônomas", 
            "Matemática Computacional", 
            "Teoria do Grafos"
        ])
        self.subject_combo.setStyleSheet("background-color: white; color: black; padding: 5px;")
        self.subject_combo.currentTextChanged.connect(self.update_professors)

        # Título para o ComboBox de professores
        professor_label = QLabel("PROFESSOR(A):")
        professor_label.setAlignment(Qt.AlignCenter)
        professor_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # ComboBox para seleção do professor
        self.professor_combo = QComboBox()
        self.professor_combo.setStyleSheet("background-color: white; color: black; padding: 5px;")

        # Botão de confirmação
        confirm_button = QPushButton("CONFIRMAR")
        confirm_button.setStyleSheet("background-color: black; color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        confirm_button.clicked.connect(self.open_confirmation_window)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(image_label)
        layout.addWidget(title_label)
        layout.addWidget(self.subject_combo)
        layout.addWidget(professor_label)
        layout.addWidget(self.professor_combo)
        layout.addWidget(confirm_button)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        # Dicionário de professores por matéria
        self.professors_by_subject = {
            "Pogramação Orientada a Objetos": ["Renato Corgosinho"],
            "Arquitetura e Organização de Computadores": ["Paulo Roberto"],
            "Estrutura de Dados": ["Kleber"],
            "Cálculo II": ["Luciana"],
            "Linguagens Formais e Autônomas": ["Paulo Roberto"],
            "Matemática Computacional": ["Jairo Dallaqua"],
            "Teoria do Grafos": ["José Luis"]
        }
        self.update_professors(self.subject_combo.currentText())

    def update_professors(self, subject):
        """Atualiza os professores no ComboBox de acordo com a matéria selecionada."""
        self.professor_combo.clear()
        if subject in self.professors_by_subject:
            self.professor_combo.addItems(self.professors_by_subject[subject])

    def open_confirmation_window(self):
        """Abre a janela de confirmação com a matéria e professor selecionados."""
        subject = self.subject_combo.currentText()
        professor = self.professor_combo.currentText()
        self.confirmation_window = ConfirmationWindow(subject, professor)
        self.confirmation_window.show()


class ConfirmationWindow(QWidget):
    def __init__(self, subject, professor):
        super().__init__()

        self.setWindowTitle("Confirmação de Presença")
        self.setGeometry(150, 150, 400, 300)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #f6eee0, 
                    stop:1 #8e9eab
                ); 
                color: black;
            }
        """)

        layout = QVBoxLayout()

        title_label = QLabel(f"{subject}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(title_label)

        professor_label = QLabel(f"Professor(a): {professor}")
        professor_label.setAlignment(Qt.AlignCenter)
        professor_label.setStyleSheet("font-size: 16px; color: white;")
        layout.addWidget(professor_label)

        fingerprint_label = QLabel("Insira sua digital:")
        fingerprint_label.setAlignment(Qt.AlignCenter)
        fingerprint_label.setStyleSheet("font-size: 14px; color: white;")
        layout.addWidget(fingerprint_label)

        fingerprint_input = QLineEdit()
        fingerprint_input.setEchoMode(QLineEdit.Password)
        fingerprint_input.setPlaceholderText("Simulação de entrada de digital")
        fingerprint_input.setStyleSheet("padding: 8px; font-size: 14px; color: black; background-color: white;")
        layout.addWidget(fingerprint_input)

        confirm_button = QPushButton("Confirmar Presença")
        confirm_button.setStyleSheet("background-color: black; color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        confirm_button.clicked.connect(self.close)
        layout.addWidget(confirm_button)

        # Botão "Finalizar Chamada"
        finish_button = QPushButton("Finalizar Chamada")
        finish_button.setStyleSheet("background-color: red; color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        finish_button.clicked.connect(QApplication.quit)
        layout.addWidget(finish_button)

        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        self.setLayout(layout)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    hud_app = HUDApp()
    hud_app.show()
    sys.exit(app.exec_())
