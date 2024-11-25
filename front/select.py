from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
import cv2
import mysql.connector
import numpy as np

# Caminho para os dados faciais registrados
face_data_dir = "face_data"

# Conexão com o banco de dados
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="AIBOLSONARO123@",  # Altere para sua senha MySQL
        database="presenca"
    )

# Função para adicionar aluno e foto ao banco de dados
def adicionar_aluno(nome, caminho_foto):
    conn = conectar_db()
    cursor = conn.cursor()
    with open(caminho_foto, 'rb') as f:
        foto_binaria = f.read()
    query = "INSERT INTO alunos (nome, foto) VALUES (%s, %s)"
    try:
        cursor.execute(query, (nome, foto_binaria))
        conn.commit()
        print(f"Aluno {nome} sincronizado com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao sincronizar {nome}: {err}")
    finally:
        cursor.close()
        conn.close()

# Sincroniza face_data com o banco de dados
def sincronizar_face_data_com_db():
    print("Sincronizando dados da pasta face_data com o banco de dados...")
    for nome in os.listdir(face_data_dir):
        pessoa_dir = os.path.join(face_data_dir, nome)
        if os.path.isdir(pessoa_dir):
            for foto_nome in os.listdir(pessoa_dir):
                caminho_foto = os.path.join(pessoa_dir, foto_nome)
                if os.path.isfile(caminho_foto):
                    adicionar_aluno(nome, caminho_foto)
    print("Sincronização concluída!")

# Reconhecimento facial
def reconhecer_rosto():
    print("Iniciando reconhecimento facial...")
    video_capture = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Erro ao acessar a webcam.")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow("Reconhecimento Facial", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Pressione 'q' para sair
            break
    video_capture.release()
    cv2.destroyAllWindows()
    print("Reconhecimento facial finalizado!")

# Cadastro de rosto
def cadastrar_rosto(nome):
    print(f"Iniciando cadastro de rosto para {nome}...")
    video_capture = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    person_dir = os.path.join(face_data_dir, nome)
    if not os.path.exists(person_dir):
        os.makedirs(person_dir)
    count = 0
    while count < 5:
        ret, frame = video_capture.read()
        if not ret:
            print("Erro ao acessar a webcam.")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_roi = gray[y:y + h, x:x + w]
            face_path = os.path.join(person_dir, f"face_{count}.jpg")
            cv2.imwrite(face_path, face_roi)
            count += 1
        cv2.imshow("Cadastro de Rosto", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 5:
            break
    video_capture.release()
    cv2.destroyAllWindows()
    print(f"Cadastro de rosto concluído para {nome}!")

class HUDApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Seleção de Matéria")
        self.setGeometry(100, 100, 400, 600)

        # Imagem no topo
        image_label = QLabel()
        pixmap = QPixmap("unespar.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(300, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # ComboBox de Matérias
        title_label = QLabel("SELECIONE A MATÉRIA:")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.subject_combo = QComboBox()
        self.subject_combo.setStyleSheet("background-color: white; padding: 5px;")
        self.subject_combo.addItems([
            "Pogramação Orientada a Objetos",
            "Arquitetura e Organização de Computadores",
            "Estrutura de Dados",
            "Cálculo II",
            "Linguagens Formais e Autônomas",
            "Matemática Computacional",
            "Teoria do Grafos"
        ])
        self.subject_combo.currentTextChanged.connect(self.update_professors)

        # Professores
        professor_label = QLabel("PROFESSOR(A):")
        professor_label.setAlignment(Qt.AlignCenter)
        professor_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.professor_combo = QComboBox()
        self.professor_combo.setStyleSheet("background-color: white; padding: 5px;")

        # Campo de Nome
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Digite o nome para cadastro")
        self.name_input.setStyleSheet("padding: 5px; font-size: 14px;")

        # Botões
        sync_button = QPushButton("ATUALIZAR DB")
        sync_button.setStyleSheet("background-color: blue; color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        sync_button.clicked.connect(sincronizar_face_data_com_db)

        recognize_button = QPushButton("RECONHECER ROSTO")
        recognize_button.setStyleSheet("background-color: green; color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        recognize_button.clicked.connect(reconhecer_rosto)

        register_button = QPushButton("CADASTRAR ROSTO")
        register_button.setStyleSheet("background-color: greenblack; color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        register_button.clicked.connect(self.cadastrar_rosto)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(image_label)
        layout.addWidget(title_label)
        layout.addWidget(self.subject_combo)
        layout.addWidget(professor_label)
        layout.addWidget(self.professor_combo)
        layout.addWidget(self.name_input)
        layout.addWidget(sync_button)
        layout.addWidget(recognize_button)
        layout.addWidget(register_button)
        self.setLayout(layout)

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
        self.professor_combo.clear()
        if subject in self.professors_by_subject:
            self.professor_combo.addItems(self.professors_by_subject[subject])

    def cadastrar_rosto(self):
        nome = self.name_input.text().strip()
        if not nome:
            print("Por favor, insira um nome para cadastro.")
            return
        cadastrar_rosto(nome)

if __name__ == '__main__':
    app = QApplication([])
    window = HUDApp()
    window.show()
    app.exec_()
