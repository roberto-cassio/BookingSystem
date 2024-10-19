from django.db import models

'''class Administrator(models.Model):
    nome = models.CharField(max_length = 100)
    email = models.EmailField(blank = False)
    password = models.CharField(max_length = 50)


    def __str__(self):
        return self.nome
'''

class Reserva(models.Model):
    name = models.CharField(max_length = 100, blank = False)
    phone = models.CharField(max_length = 14, blank = False)
    num_people = models.IntegerField(blank = False)
    datetime = models.DateTimeField(blank = False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    deleted_by = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null= True, blank=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
class Table(models.Model):
    size = models.IntegerField(blank=False)
    name = models.CharField(max_length = 30, blank = False)
    updated_by = models.CharField(max_length=50, blank=True, null=True)
    deleted_by = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null= True, blank=True)
    deleted_at = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return self.name