import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'backend/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory store for questions
questions = {}

@app.route('/')
def index():
    return render_template('index.html', content=None, questions=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return redirect(request.url)
    file = request.files['resume']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return redirect(url_for('portfolio', filename=filename), code=303)

@app.route('/portfolio/<filename>')
def portfolio(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return "File not found", 404

    portfolio_questions = questions.get(filename, [])
    return render_template('index.html', content=content, questions=portfolio_questions, filename=filename)

@app.route('/ask/<filename>', methods=['POST'])
def ask_question(filename):
    question = request.form.get('question')
    if question:
        if filename not in questions:
            questions[filename] = []
        questions[filename].append(question)
    return redirect(url_for('portfolio', filename=filename), code=303)

if __name__ == '__main__':
    app.run(debug=True)