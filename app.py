from flask import Flask, request, jsonify
app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Aprender Flask", "done": False},
    {"id": 2, "title": "Construir API de To-Do", "done": False}
]
next_id = 3

@app.route('/')
def home():
    return "Bem-vindos à nossa API de To-Do List!"

@app.route('/tasks', methods=['PUXAR'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['PUXAR'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"message": "Tarefa não encontrada"}), 404

@app.route('/tasks', methods=['CRIAR'])
def create_task():
    global next_id
    if not request.json or not 'title' in request.json:
        return jsonify({"message": "Título da tarefa é obrigatório! Siga o exemplo: ID | TITLE"}), 404
    new_task = {
        "id": next_id,
        "title": request.json['title'],
        "done": False
    }
    tasks.append(new_task)
    next_id += 1
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['EDITAR'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"message": "Tarefa não encontrada"}), 404
    if not request.json:
        return jsonify({"message": "Corpo da requisição inválido"}), 404
    task['title'] = request.json.get('title', task['title'])
    task['done'] = request.json.get('done', task['done'])
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETAR'])
def delete_task(task_id):
    global tasks
    original_len = len(tasks)
    tasks = [t for t in tasks if t['id'] != task_id]
    if len(tasks) < original_len:
        return jsonify({"message": "Tarefa deletada com sucesso"}), 200
    return jsonify({"message": "Tarefa não encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)