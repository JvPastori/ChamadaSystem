from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

# Classe principal que exibe a janela para seleção de matéria e professor
class HUDApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()  # Inicializa a interface do usuário

    def init_ui(self):
        # Configurações da janela principal
        self.setWindowTitle("Seleção de Matéria")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: ##f6eee0; color: white;")

        # Título da seleção de matéria
        title_label = QLabel("SELECIONE A MATÉRIA:")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # ComboBox de Matérias (opções para escolher)
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(["Pogramação Orientada a Objetos", "Arquitetura e Organização de Computadores", "Estrutura de Dados", "Cálculo II", "Linguagens Formais e Autônomas", "Matemática Computacional", "Teoria do Grafos" ])  # Matérias disponíveis
        self.subject_combo.setStyleSheet("background-color: white; color: black; padding: 5px;")
        # Conecta a mudança de seleção de matéria à atualização de professores
        self.subject_combo.currentTextChanged.connect(self.update_professors)

        # Título para o ComboBox de professores
        professor_label = QLabel("PROFESSOR(A):")
        professor_label.setAlignment(Qt.AlignCenter)
        professor_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # ComboBox para seleção do professor (atualizado conforme a matéria)
        self.professor_combo = QComboBox()
        self.professor_combo.setStyleSheet("background-color: white; color: black; padding: 5px;")

        # Botão de confirmação para abrir a janela de confirmação
        confirm_button = QPushButton("CONFIRMAR")
        confirm_button.setStyleSheet("background-color: black; color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        confirm_button.clicked.connect(self.open_confirmation_window)  # Conecta o clique ao método para abrir nova janela

        # Layout principal para organizar os widgets
        layout = QVBoxLayout()
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
            "Práticas Extensionistas": ["Lisandro Modesto"],
            "Teoria do Grafos": ["José Luis"]
        }
        # Inicializa a lista de professores para a matéria selecionada inicialmente
        self.update_professors(self.subject_combo.currentText())

    def update_professors(self, subject):
        """Atualiza os professores no ComboBox de acordo com a matéria selecionada."""
        self.professor_combo.clear()  # Limpa o ComboBox de professores
        if subject in self.professors_by_subject:
            # Adiciona os professores correspondentes à matéria selecionada
            self.professor_combo.addItems(self.professors_by_subject[subject])

    def open_confirmation_window(self):
        """Abre a janela de confirmação com a matéria e professor selecionados."""
        # Obtém a matéria e professor atuais selecionados
        subject = self.subject_combo.currentText()
        professor = self.professor_combo.currentText()
        
        # Cria e exibe uma nova instância da janela de confirmação
        self.confirmation_window = ConfirmationWindow(subject, professor)
        self.confirmation_window.show()

# Classe da janela de confirmação que exibe a matéria, professor e campo para digital
class ConfirmationWindow(QWidget):
    def __init__(self, subject, professor):
        super().__init__()
        
        # Configurações básicas da janela
        self.setWindowTitle("Confirmação de Presença")
        self.setGeometry(150, 150, 400, 300)
        self.setStyleSheet("background-color: ##f6eee0; color: black;")

        # Criação do layout da janela
        layout = QVBoxLayout()

        # Título da janela
        title_label = QLabel(f"{subject}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # Exibe o professor selecionado
        professor_label = QLabel(f"Professor(a): {professor}")
        professor_label.setAlignment(Qt.AlignCenter)
        professor_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(professor_label)

        # Label para o campo de inserção de digital
        fingerprint_label = QLabel("Insira sua digital:")
        fingerprint_label.setAlignment(Qt.AlignCenter)
        fingerprint_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(fingerprint_label)

        # Campo de entrada de texto para simular a inserção de digital
        fingerprint_input = QLineEdit()
        fingerprint_input.setEchoMode(QLineEdit.Password)  # Esconde o texto digitado
        fingerprint_input.setPlaceholderText("Simulação de entrada de digital")
        fingerprint_input.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(fingerprint_input)

        # Botão de confirmação de presença
        confirm_button = QPushButton("Confirmar Presença")
        confirm_button.setStyleSheet("background-color: black; color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        confirm_button.clicked.connect(self.close)  # Fecha a janela ao confirmar
        layout.addWidget(confirm_button)

        # Configurações do layout
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        self.setLayout(layout)

if __name__ == "__main__":
    import sys
    # Criação e execução da aplicação
    app = QApplication(sys.argv)
    hud_app = HUDApp()
    hud_app.show()
    sys.exit(app.exec_())
