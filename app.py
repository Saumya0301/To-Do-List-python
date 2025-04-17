from flask import Flask, render_template, request,redirect
import sqlite3,datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              content TEXT NOT NULL,
              is_done BOOLEAN DEFAULT 0)
              ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    day_of_week = datetime.datetime.now().weekday()
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks = tasks, day_of_week=day_of_week)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content']
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/done/<int:task_id>', methods=['POST'])
def done(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET is_done = 1 WHERE id =?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug = True)