# converter/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TextForm
import os


def convert_text_to_latex(text):
    # Простой шаблон LaTeX
    return r"""
\documentclass{article}
\begin{document}
%s
\end{document}
""" % text


def home(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            latex_content = convert_text_to_latex(text)

            # Сохраняем файл .tex
            filename = "document.tex"
            filepath = os.path.join('downloads', filename)

            # Создаем директорию для загрузок, если она не существует
            os.makedirs('downloads', exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(latex_content)

            return redirect('download_file')
    else:
        form = TextForm()

    return render(request, 'converter/index.html', {'form': form})


def download_file(request):
    filename = "document.tex"
    filepath = os.path.join('downloads', filename)

    with open(filepath, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/x-tex')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response