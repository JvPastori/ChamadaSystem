from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QLineEdit, QDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
import cv2
import numpy as np
import time

# Caminho para os dados faciais registrados
face_data_dir = "face_data"

# Função para carregar rostos cadastrados no face_data
def carregar_rostos_cadastrados():
    faces = []
    ids = []
    pessoas = []  # Lista para armazenar os nomes das pessoas
    for pessoa_dir in os.listdir(face_data_dir):
        pessoa_path = os.path.join(face_data_dir, pessoa_dir)
        if os.path.isdir(pessoa_path):
            for foto_nome in os.listdir(pessoa_path):
                caminho_foto = os.path.join(pessoa_path, foto_nome)
                if os.path.isfile(caminho_foto):
                    imagem = cv2.imread(caminho_foto, cv2.IMREAD_GRAYSCALE)
                    faces.append(imagem)
                    ids.append(pessoa_dir)  # Adicionando nome da pessoa
                    pessoas.append(pessoa_dir)  # Lista com os nomes das pessoas
    return faces, ids, pessoas

# Função para treinar o classificador
def treinar_classificador(faces, ids):
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(faces, np.array(ids))
    return model

# Função para cadastrar um rosto
def cadastrar_rosto(nome):
    print(f"Iniciando cadastro de rosto para {nome}...")

    # Abertura da webcam
    video_capture = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Criar diretório para a pessoa, caso não exista
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
        faces_detectadas = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces_detectadas:
            # Desenha o retângulo ao redor do rosto
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_roi = gray[y:y + h, x:x + w]
            face_path = os.path.join(person_dir, f"face_{count}.jpg")
            cv2.imwrite(face_path, face_roi)
            count += 1

        # Exibe a janela com a webcam
        cv2.imshow("Cadastro de Rosto", frame)

        # Permite sair do loop com a tecla 'q' ou após 5 fotos
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 5:
            break

    video_capture.release()
    cv2.destroyAllWindows()
    print(f"Cadastro de rosto concluído para {nome}!")

# Função para reconhecer rostos
def reconhecer_rosto():
    print("Iniciando reconhecimento facial...")

    # Carregar rostos cadastrados
    faces, ids, pessoas = carregar_rostos_cadastrados()

    if len(faces) == 0:
        print("Nenhum rosto cadastrado encontrado!")
        return

    # Mapear os nomes para números (ID numérico)
    ids_map = {pessoa: i for i, pessoa in enumerate(set(ids))}
    ids_numericos = [ids_map[pessoa] for pessoa in ids]

    # Treinar o modelo com os rostos cadastrados
    model = treinar_classificador(faces, np.array(ids_numericos))

    # Inicializar webcam
    video_capture = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Erro ao acessar a webcam.")
            break

        # Converter a imagem para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostos na imagem
        faces_detectadas = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces_detectadas:
            # Capturar a região do rosto
            face_roi = gray[y:y+h, x:x+w]

            # Reconhecer o rosto
            id_, confidence = model.predict(face_roi)

            # Verificar se a confiança é alta (menor é melhor)
            if confidence < 100:
                nome = list(ids_map.keys())[list(ids_map.values()).index(id_)]
                confidence_text = f"Confiança: {round(100 - confidence)}%"
            else:
                nome = "Desconhecido"
                confidence_text = f"Confiança: {round(100 - confidence)}%"

            # Desenhar um retângulo ao redor do rosto e colocar o nome
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{nome} {confidence_text}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Exibir a imagem com a detecção e reconhecimento
        cv2.imshow("Reconhecimento Facial", frame)

        # Sair da webcam quando pressionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar a captura de vídeo e fechar janelas
    video_capture.release()
    cv2.destroyAllWindows()
    print("Reconhecimento facial finalizado!")

# Nova janela para mostrar alunos cadastrados

class AlunosWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alunos Cadastrados")
        self.setGeometry(100, 100, 400, 400)

        # Layout da janela de alunos
        layout = QVBoxLayout()

        # Tabela de alunos com checkbox
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)  # Duas colunas: ID e Checkbox
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Selecionado"])

        # Carregar os alunos e adicionar na tabela
        alunos = self.carregar_nomes_alunos()
        alunos.sort()  # Ordenar os alunos em ordem alfabética
        self.tableWidget.setRowCount(len(alunos))

        for row, aluno in enumerate(alunos):
            # Adicionar o ID do aluno na primeira coluna (não editável)
            item_nome = QTableWidgetItem(aluno)
            item_nome.setFlags(Qt.ItemIsEnabled)  # Impede a edição do nome
            self.tableWidget.setItem(row, 0, item_nome)

            # Adicionar checkbox na segunda coluna
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.tableWidget.setItem(row, 1, checkbox_item)

        # Layout da janela
        layout.addWidget(self.tableWidget)

        # Botão para reconhecer rostos
        recognize_button = QPushButton("Reconhecer Rosto")
        recognize_button.setStyleSheet("background-color: blue; color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        recognize_button.clicked.connect(self.reconhecer_rosto)  # Conecta o botão à função reconhecer_rosto

        layout.addWidget(recognize_button)  # Adiciona o botão de reconhecimento no layout

        self.setLayout(layout)

    def carregar_nomes_alunos(self):
        alunos = []
        for pessoa_dir in os.listdir(face_data_dir):
            pessoa_path = os.path.join(face_data_dir, pessoa_dir)
            if os.path.isdir(pessoa_path):
                alunos.append(pessoa_dir)
        return alunos

    def reconhecer_rosto(self):
        print("Iniciando reconhecimento facial...")

        # Carregar rostos cadastrados
        faces, ids, pessoas = carregar_rostos_cadastrados()

        if len(faces) == 0:
            print("Nenhum rosto cadastrado encontrado!")
            return

        # Mapear os nomes para números (ID numérico)
        ids_map = {pessoa: i for i, pessoa in enumerate(set(ids))}
        ids_numericos = [ids_map[pessoa] for pessoa in ids]

       
