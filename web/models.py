from django.db import models
from django.utils import timezone
from datetime import date

# Create your models here.

class Rol(models.Model):
	name = models.CharField(max_length=30)
	path = models.CharField(max_length=30, default="index.html")
	def __str__(self) -> str:
		return self.name + " | " + self.path

class Type(models.Model):
	name = models.CharField(max_length=30)
	def __str__(self) -> str:
		return self.name 

class Usuario(models.Model):
	uname  = models.CharField(max_length=30)
	ulname = models.CharField(max_length=30)
	passwd = models.CharField(max_length=65)
	email = models.EmailField(max_length=65)
	rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
	last_login = models.DateTimeField( default=timezone.now)
	auth_token = models.CharField(max_length=65, default="")
	def __str__(self) -> str:
		return self.uname + " | " + self.email

class Actividad(models.Model):
	uname  = models.CharField(max_length=30)
	type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
	date = models.DateField(default=date.today)
	def __str__(self) -> str:
		return self.uname

class Evidence(models.Model):
	event = models.ForeignKey(Actividad, on_delete=models.SET_NULL, null=True)
	uname = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, limit_choices_to={'rol__name': "Estudiante"})
	att = models.BooleanField(default=True)
	recog = models.CharField(max_length=30 ,default="")
	doc = models.ImageField(upload_to="webapp/static/public/", default="/img_default")
	def __str__(self) -> str:
		return self.event.__str__() + " " + self.uname.__str__() + " " + self.recog

