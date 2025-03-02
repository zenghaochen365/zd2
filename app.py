from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# 初始化数据库
def init_db():
    conn = sqlite3.connect('zengdoing.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    completed INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

# 获取所有任务
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('zengdoing.db')
    c = conn.cursor()
    c.execute("SELECT id, task, completed FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return jsonify(tasks)

# 添加任务
@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json.get('task')
    if task:
        conn = sqlite3.connect('zengdoing.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "任务不能为空"}), 400

# 标记任务完成
@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    conn = sqlite3.connect('zengdoing.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# 删除任务
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('zengdoing.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# 首页
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)