from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta: #Para definir el modelo asociado al formulario y los campos que se van a mostrar
        model = Task
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':3})
        }