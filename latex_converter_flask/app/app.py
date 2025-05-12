from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
import os
from docx import Document

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Создаем папку для загрузок, если ее еще нет
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class UploadForm(FlaskForm):
    file = FileField('Upload Word Document', validators=[DataRequired()])
    submit = SubmitField('Convert to LaTeX')

def convert_docx_to_latex(docx_file_path):
    document = Document(docx_file_path)
    latex_lines = []

    for paragraph in document.paragraphs:
        latex_lines.append(paragraph.text)  # Простой пример без форматирования

    latex_content = '\n'.join(latex_lines)
    return latex_content

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        uploaded_file = form.file.data
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)

        latex_content = convert_docx_to_latex(file_path)
        return render_template('result.html', latex_content=latex_content)

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)