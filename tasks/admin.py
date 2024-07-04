from django.contrib import admin

#traer el modelo tarea para admin
from .models import Task

# clase para poder ver el campo de solo lectura desde el panel
class Taskadmin(admin.ModelAdmin):
    #enviar los campos de lectura para verlos en pantalla desde admin: 
    readonly_fields = ('created' , ) #agregarle  si o si la  coma porque recibe una tupla

# Register your models here.
#los parametros que le pasamos son los que queremos visualizar
admin.site.register(Task, Taskadmin)

