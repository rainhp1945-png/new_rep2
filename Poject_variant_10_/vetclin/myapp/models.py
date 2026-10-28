from django.db import models

# Create your models here.

class Owner(models.Model):
        id = models.AutoField(primary_key=True)
        FIO = models.TextField()
        Phone = models.IntegerField()
        Adres = models.TextField()

        def __str__(self):
            return f'{self.id}{self.FIO} {self.Phone} ({self.Adres})'

class Animal(models.Model):
    id = models.AutoField(primary_key=True)
    Nickname = models.TextField(max_length=100)
    Type = models.TextField()
    Poroda = models.TextField()
    Owner_id = models.ForeignKey(Owner, on_delete=models.CASCADE,related_name='Animal', verbose_name='Owner')
    def __str__(self):
        return f'{self.id}{self.Type} {self.Poroda} {self.Nickname} {self.Owner_id}'

class Reception(models.Model):
    id = models.AutoField(primary_key=True)
    Date = models.DateTimeField(auto_now_add=True)
    Diagnoz = models.TextField()
    Treat = models.TextField()
    Dublicat = models.TextField()
    Animal = models.ForeignKey(Animal, on_delete=models.CASCADE,related_name='Reception', verbose_name='Animal')
    def __str__(self):
        return f'{self.id} {self.Date} {self.Diagnoz} {self.Treat} {self.Dublicat} {self.Animal_id}'

class Service(models.Model):
    id = models.AutoField(primary_key=True)
    Name = models.TextField(max_length=100)
    Price = models.IntegerField()
    Reception_id= models.ForeignKey(Reception, on_delete=models.CASCADE,related_name='Service', verbose_name='Reception')
    def __str__(self):
        return f'{self.id} {self.Name} {self.Price} {self.Reception_id}'