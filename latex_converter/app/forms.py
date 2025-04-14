# converter/forms.py
from django import forms

class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Введите текст для преобразования в LaTeX')