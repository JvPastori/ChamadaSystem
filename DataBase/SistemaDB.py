CREATE TABLE usuarios (
    ra VARCHAR(20) PRIMARY KEY, -- Registro Acadêmico do Aluno
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    data_nascimento DATE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE biometria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ra VARCHAR(20), -- Relacionado ao RA do aluno
    hash_biometria VARCHAR(256) NOT NULL, -- Código hash gerado da biometria
    FOREIGN KEY (ra) REFERENCES usuarios(ra) ON DELETE CASCADE
);
CREATE TABLE materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    professor VARCHAR(100) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE aluno_materia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ra VARCHAR(20), -- Registro do Aluno
    materia_id INT,
    FOREIGN KEY (ra) REFERENCES usuarios(ra) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
);
CREATE TABLE presencas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ra VARCHAR(20), -- Registro do Aluno
    materia_id INT,
    data_presenca DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('presente', 'ausente') DEFAULT 'presente',
    FOREIGN KEY (ra) REFERENCES usuarios(ra) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
);

# cadastro aluno
INSERT INTO usuarios (ra, nome, email, telefone, data_nascimento) 
VALUES ('202312345', 'Gabriel Ricetto', 'gabriel@email.com', '1234567890', '1995-05-15');

#biometria

INSERT INTO biometria (ra, hash_biometria) 
VALUES ('202312345', 'abc123hashgeradopelaleitoraqui');

#insercao de materias

INSERT INTO materias (nome, professor) 
VALUES 
('Matemática', 'Prof. Luciana'),
('Física', 'Prof. Guilherme');

#Cadastro na materia

-- Associar Gabriel à Matemática
INSERT INTO aluno_materia (ra, materia_id) 
VALUES ('202312345', 1);

-- Associar Gabriel à Física
INSERT INTO aluno_materia (ra, materia_id) 
VALUES ('202312345', 2);

#Presença

-- Presença de Gabriel em Matemática
INSERT INTO presencas (ra, materia_id, status) 
VALUES ('202312345', 1, 'presente');

#consulta de aluno matriculado em uma materia

SELECT u.ra, u.nome AS aluno, m.nome AS materia
FROM aluno_materia am
JOIN usuarios u ON am.ra = u.ra
JOIN materias m ON am.materia_id = m.id
WHERE m.nome = 'Matemática';


#presenca na materia

SELECT u.ra, u.nome AS aluno, m.nome AS materia, p.data_presenca, p.status
FROM presencas p
JOIN usuarios u ON p.ra = u.ra
JOIN materias m ON p.materia_id = m.id
WHERE u.ra = '202312345' AND m.nome = 'Matemática';

#listar presenca por materia

SELECT m.nome AS materia, u.nome AS aluno, p.data_presenca, p.status
FROM presencas p
JOIN usuarios u ON p.ra = u.ra
JOIN materias m ON p.materia_id = m.id
ORDER BY m.nome, p.data_presenca;

#integracao em python

import hashlib
import mysql.connector

# Exemplo de biometria capturada
biometria = "dados_da_digital"

# Gerar o hash da biometria
hash_biometria = hashlib.sha256(biometria.encode()).hexdigest()

# Conectar ao banco de dados
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sua_senha",
    database="chamada_biometria"
)
cursor = conn.cursor()

# Inserir o hash no banco
cursor.execute("""
    INSERT INTO biometria (ra, hash_biometria)
    VALUES (%s, %s)
""", ('202312345', hash_biometria))

conn.commit()
cursor.close()
conn.close()
