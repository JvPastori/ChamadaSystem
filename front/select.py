from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QLineEdit, QDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
import cv2
import numpy as np
import mysql.connector
from mysql.connector import Error

# Configuração do banco de dados
db_config = {
    'host': 'localhost',
    'database': 'chamadasystem',
    'user': 'root',
    'password': '159621'
}

def conectar_banco():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Conexão com o banco de dados estabelecida.")
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

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

import time

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

        # Treinar o modelo com os rostos cadastrados
        model = treinar_classificador(faces, np.array(ids_numericos))

        # Inicializar webcam
        self.video_capture = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

        self.is_running = True  # Variável de controle para o loop de reconhecimento

        while self.is_running:
            ret, frame = self.video_capture.read()
            if not ret:
                print("Erro ao acessar a webcam.")
                break

            # Converter a imagem para escala de cinza
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detectar rostos na imagem
            faces_detectadas = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces_detectadas:
                # Capturar a região do rosto
                face_roi = gray[y:y+h, x:x+w]

                # Reconhecer o rosto
                id_, confidence = model.predict(face_roi)

                # Verificar se a confiança é alta (menor é melhor)
                if confidence < 100:
                    nome = list(ids_map.keys())[list(ids_map.values()).index(id_)]
                    confidence_text = f"Confiança: {round(100 - confidence)}%"

                    # Marcar o checkbox correspondente ao aluno na tabela
                    self.marcar_checkbox(nome)
                    
                    # Aguardar 2 segundos antes de fechar
                    print(f"Face de {nome} reconhecida. Esperando 2 segundos antes de fechar a janela...")
                    time.sleep(2)  # Espera 2 segundos

                    # Após o atraso, fecha a janela da webcam
                    self.fechar_webcam()
                    return  # Interrompe o loop de reconhecimento após o reconhecimento de um rosto
                else:
                    nome = "Desconhecido"
                    confidence_text = f"Confiança: {round(100 - confidence)}%"

                # Desenhar um retângulo ao redor do rosto e colocar o nome
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"{nome} {confidence_text}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

            # Exibir a imagem com a detecção e reconhecimento
            cv2.imshow("Reconhecimento Facial", frame)

            # Aguardar uma chave de interrupção para parar o reconhecimento (opcional)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Reconhecimento interrompido com 'q'.")
                break

        # Liberar a captura de vídeo e fechar janelas
        self.fechar_webcam()

    def marcar_checkbox(self, nome):
        """
        Marca o checkbox do aluno correspondente ao nome encontrado
        """
        # Buscar o aluno na tabela e marcar o checkbox
        for row in range(self.tableWidget.rowCount()):
            aluno = self.tableWidget.item(row, 0).text()  # Obtém o nome do aluno na tabela
            if aluno == nome:
                checkbox_item = self.tableWidget.item(row, 1)
                checkbox_item.setCheckState(Qt.Checked)
                print(f"Aluno {nome} reconhecido e checkbox marcado!")
                return

    def fechar_webcam(self):
        """
        Função para liberar a captura de vídeo e fechar a janela do OpenCV.
        """
        if self.video_capture.isOpened():
            self.video_capture.release()  # Liberar a captura da webcam
        cv2.destroyAllWindows()  # Fechar todas as janelas do OpenCV

    def closeEvent(self, event):
        """
        Fechar a janela da webcam corretamente quando a janela principal for fechada.
        """
        self.is_running = False  # Interromper o loop da webcam
        self.fechar_webcam()  # Fechar a webcam
        event.accept()  # Aceitar o evento de fechar a janela


# Código do front-end
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
            "Programação Orientada a Objetos",
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
        register_button = QPushButton("CADASTRAR ROSTO")
        register_button.setStyleSheet("background-color: green; color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        register_button.clicked.connect(self.cadastrar_rosto)

        
        show_students_button = QPushButton("REALIZAR CHAMADA")
        show_students_button.setStyleSheet("background-color: blue; color: white; font-size: 14px; font-weight: bold; padding: 10px;")
        show_students_button.clicked.connect(self.show_students)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(image_label)
        layout.addWidget(title_label)
        layout.addWidget(self.subject_combo)
        layout.addWidget(professor_label)
        layout.addWidget(self.professor_combo)
        layout.addWidget(self.name_input)
        layout.addWidget(register_button)
        layout.addWidget(show_students_button)
        self.setLayout(layout)

        self.professors_by_subject = {
            "Programação Orientada a Objetos": ["Renato Corgosinho"],
            "Arquitetura e Organização de Computadores": ["Paulo Roberto"],
            "Estrutura de Dados": ["Kleber"],
            "Cálculo II": ["Luciana"],
            "Linguagens Formais e Autônomas": ["Paulo Roberto"],
            "Matemática Computacional": ["Jairo Dallaqua"],
            "Teoria do Grafos": ["José Luis"]
        }
        self.update_professors(self.subject_combo.currentText())

    def update_professors(self, subject):
        # Atualiza a lista de professores com base na matéria selecionada
        self.professor_combo.clear()
        self.professor_combo.addItems(self.professors_by_subject.get(subject, []))

    def cadastrar_rosto(self):
        nome = self.name_input.text().strip()
        if not nome:
            print("Por favor, insira um nome para cadastro.")
            return
        cadastrar_rosto(nome)

    def reconhecer_rosto(self):
        reconhecer_rosto()

    def show_students(self):
        # Exibe a janela de alunos cadastrados
        alunos_window = AlunosWindow()
        alunos_window.exec_()

if __name__ == '__main__':
    app = QApplication([])
    window = HUDApp()
    window.show()
    app.exec_()
