from django.db import models

#importar user para el foreign key
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    #se autogenera sin necesidad de pasarlo
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True) # blank=true / opcional para el admin pero el null para la db dice que si debe añadirse
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #codigo para ver desde admin el nombre de la tarea
    #cuando usen ese modelo va a retornar title y user name en str
    def __str__(self):
        return self.title + "- by " + self.user.username
        
    

    