from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


conn = sqlite3.connect('gestao_medicamentos.db')
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicamentos(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL,
               idade FLOAT,
               sexo TEXT,
               farmacia TEXT,
               endereco TEXT,
               telefone TEXT
    ) 
""")

conn.commit()
conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect('gestao_medicamentos.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM medicamentos')
    medicamentos = cursor.fetchall()
    conn.close()
    return render_template('index.html', medicamentos=medicamentos)

@app.route('/novo_medicamento', methods=['GET', 'POST'])
def novo_medicamento():
    if request.method == 'POST':
        nome = request.form['nome']
        idade= request.form['idade']
        sexo = request.form['sexo']
        farmacia = request.form['farmacia']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        conn = sqlite3.connect('gestao_medicamentos.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO medicamentos (nome, idade, sexo, farmacia, endereco, telefone)
                       VALUES (?, ?, ?, ?, ?, ?)
""", (nome, idade, sexo, farmacia, endereco, telefone))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('novo_medicamento.html')



@app.route('/limpar_medicamento')
def limpar_medicamento():
    conn = sqlite3.connect('gestao_medicamentos.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM medicamentos')
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main':
    app.run(debug=True)
    