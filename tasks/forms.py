#importar modelo de formulario de django con la clase ModelForm
from django import forms
#importar modelo que vas a usar para el formulario ( task)
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        #señalamos los campos que vamos a usar para este formulario(task):
        fields = ['title', 'description', 'important']
        widgets = {
            'title' : forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'write a title'}),
            'description' : forms.Textarea(attrs={'class' : 'form-control' ,  'placeholder' : 'write a description'}),
            'important' : forms.CheckboxInput(attrs={'class' : 'form-check-input '})
            
        }