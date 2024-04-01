from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from web.models import Usuario, Evidence, Actividad, Type, Rol
from django.utils import timezone
from django.db.models import Q
import os, hashlib, random, json
from web.views import e403, e404
from hashlib import sha256
from time import time
import csv
from io import StringIO


ALLOWED_EXTENSIONS = [
	"png",
	"jpg",
	"jpeg",
	"pdf",
]


def _get_extension(path):
    return path[-path[::-1].index('.'):]


def _prepare_photo(request):
    photo_name = request.FILES['file'].__str__()
    extension = _get_extension(photo_name)
    photo_name = sha256((photo_name + str(time())).encode()).hexdigest() + '.' + extension
    return photo_name, extension



def gen_auth_token():
	return hashlib.sha256(
		(str(timezone.now()) + str(random.randint(1111111, 99999999))).encode()
	).hexdigest()


def get_user(request, rol):
	auth_token = request.COOKIES.get("auth_token")
	user = Usuario.objects.filter(auth_token=auth_token)
	if len(user) == 0:
		return None
	else:
		if user[0].rol.name in rol:
			return user[0]
		else:
			return None


def login(request):
	if request.method != "POST":
		return e403()
	email = request.POST['email']
	passwd = request.POST['pswd']
	#try:
	user = Usuario.objects.filter(email=email,passwd=passwd)
	if len(user) == 0:
		return redirect("/src/login/login.html")
	http = redirect(user[0].rol.path)
	token = gen_auth_token()
	user[0].auth_token = token
	user[0].save()
	http.set_cookie("auth_token", token, expires=None, max_age=3000)
	return http


def logout(request):
	auth_token = request.COOKIES.get("auth_token")
	user = Usuario.objects.filter(auth_token=auth_token)
	if len(user) == 0:
		print("Logout Reached")
		return redirect("/src/login/login.html")
	user[0].auth_token = ""
	user[0].save()
	http = redirect("/src/login/login.html")
	http.delete_cookie("auth_token")
	http.delete_cookie("csrftoken")
	return http


def send_evidence(request):       #Secretaria
	user = get_user(request, ["Secretaria", "Jefe Año"])
	if user == None:
		return e403
	l = list(Evidence.objects.all().values())
	z=l
	count=0
	for i in l:
		for k in i.keys():
			if k == "event_id":
				z[count][k] = Actividad.objects.get(id=i[k]).uname
			if k == "uname_id":
				z[count][k] = Usuario.objects.get(id=i[k]).uname
		count += 1
	body = json.dumps({"evd": z})
	print(body)
	return HttpResponse(body, "application/json")


def edit_evidence(request):
	if request.method != "POST":
		return e403()
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	args = {}
	for element in request.POST.keys():
		if "id" == element:
			id = request.POST["id"]
			continue
		args[element] = request.POST[element]
	print("ASD", id, args)
	Evidence.objects.filter(id=id).update(**args)
	return redirect("/src/evidence/evidence.html")


def revidence(request):
	if request.method != "POST":
		return e403()
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	id = request.POST["id"]
	print("Deleting", id, type(id))
	Evidence.objects.filter(id=id).delete()
	return redirect("/src/evidence/evidence.html")


def send_csv(request):
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	mm = list(Evidence.objects.all().values())
	if len(mm) == 0:
		return HttpResponse("No se puede generar un CSV vacio.")
	header = mm[0].keys()
	csv_buffer = StringIO()
	writer = csv.DictWriter(csv_buffer, fieldnames=header)
	writer.writeheader()
	writer.writerows(mm)
	return HttpResponse(csv_buffer.getvalue(), "text/csv")


def subir_evidence(request):  #
	if request.method != "POST":
		return e403()
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	
	photo_name, extension = _prepare_photo(request)
	if not extension in ALLOWED_EXTENSIONS:
		return e403()
	actid = Actividad.objects.filter(id=int(request.POST["typepivotactividad"]))
	user = Usuario.objects.filter(id=int(request.POST["typepivotusername"]))
	print(actid[0].id)
	doc = "webapp/static/public/" + photo_name
	Evidence.objects.create(event=actid[0], uname=user[0], doc=doc, recog=request.POST["recog"])
	open("webapp/static/public/" + photo_name, "bw").write(request.FILES['file'].read())
	return redirect("/src/evidence/evidence.html")



def send_sactivities(request):  #
	user = get_user(request, ["Estudiante", "Jefe Año"])
	if user == None:
		return e403
	#l = list(Actividad.objects.all().values())
	activities = Actividad.objects.all()
	evidencies = Evidence.objects.all()
	l = []
	count = 0
	for activity in activities:
		dump = evidencies.filter(event=activity.id, uname=user.id)
		if len(dump) == 0:
			l.append(activities.values()[count])
		count += 1
	z=l
	
	count=0
	for i in l:
		for k in i.keys():
			if k == "type_id":
				z[count][k] = list(Type.objects.filter(id=i[k]).values())
			if k == "date":
				z[count][k] = str(i[k])
		count += 1
	body = json.dumps({"act": z})
	return HttpResponse(body, "application/json")


def send_type(request):  #
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	return HttpResponse(json.dumps(list(Type.objects.all().values())), "application/json" )


def send_rol(request):  #
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	return HttpResponse(json.dumps(list(Rol.objects.all().values())), "application/json" )


def send_activities(request):  #
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	return HttpResponse(json.dumps(list(Actividad.objects.all().values("id", "uname"))), "application/json" )

def send_users(request):  #
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	if "asd" in request.GET.keys():
		return HttpResponse(json.dumps(list(Usuario.objects.filter(Q(rol__id=0) | Q(rol__id=1)).values("id", "uname", "ulname", "email", "rol"))), "application/json" )
	return HttpResponse(json.dumps(list(Usuario.objects.filter(rol__id=0).values("id", "uname"))), "application/json" )

	
def rusers(request):
	if request.method != "POST":
		return e403()
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	id = request.POST["id"]
	print("Deleting", id, type(id))
	Usuario.objects.filter(id=id).delete()
	return redirect("/src/profiles/profiles.html")


def add_users(request):
	if request.method != "POST":
		print("asdasdasd")
		return e403()
	user = get_user(request, ["Jefe Año"])
	if user == None:
		print("ddddddd")
		return e403
	args = {}
	for element in request.POST.keys():
		if element == "rol":
			args[element] = Rol.objects.filter(id=request.POST[element])[0]
			continue
		args[element] = request.POST[element]
	usernew = Usuario(**args)
	usernew.save()
	return redirect("/src/profiles/profiles.html")


def edit_users(request):
	if request.method != "POST":
		return e403()
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	args = {}
	for element in request.POST.keys():
		if "id" == element:
			id = request.POST["id"]
			continue
		args[element] = request.POST[element]
	print("ASD", id, args)
	Usuario.objects.filter(id=id).update(**args)
	return redirect("/src/profiles/profiles.html")


def send_asistencia(request):
	def check_asistence(user,activity):
		evidencias = len(Evidence.objects.filter(Q(uname=user) & Q(event=activity)).values())
		if evidencias == 0:
			return False
		else:
			return True
	actividades = list(Actividad.objects.all())
	users = list(Usuario.objects.filter(rol__id=0))
	args = []
	for activity in actividades:
		for user in users:
			if check_asistence(user,activity):
				att = "Si"
			else:
				att = "No"
			args.append( {"event": activity.uname, "uname": user.uname, "ulname": user.ulname, "att": att} )

	return HttpResponse(json.dumps(args), "application/json")


def subir_sactivities(request):  #
	if request.method != "POST":
		return e403()
	user = get_user(request, ["Estudiante"])
	if user == None:
		return e403
	
	photo_name, extension = _prepare_photo(request)
	if not extension in ALLOWED_EXTENSIONS:
		return e403()
	actid = Actividad.objects.filter(id=int(request.POST["actid"]))
	print(actid[0].id)
	doc = "webapp/static/public/" + photo_name
	Evidence.objects.create(event=actid[0], uname=user, doc=doc)
	open("webapp/static/public/" + photo_name, "bw").write(request.FILES['file'].read())
	return redirect("/src/myevidence/myevidence.html")


def edit_sactivities(request):
	if request.method != "POST":
		return e403()
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	args = {}
	for element in request.POST.keys():
		if "id" == element:
			id = request.POST["id"]
			continue
		args[element] = request.POST[element]
	print("ASD", id, args)
	Actividad.objects.filter(id=id).update(**args)
	return redirect("/src/activities/activities.html")


def add_sactivities(request):
	if request.method != "POST":
		return e403()
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	uname = request.POST["uname"]
	type = Type.objects.filter(id=int(request.POST["type"]))[0]
	date = request.POST["Fecha"]

	Actividad.objects.create(uname=uname, type=type, date=date)


	return redirect("/src/activities/activities.html")


def ractivities(request):
	if request.method != "POST":
		return e403()
	user = get_user(request, ["Jefe Año"])
	if user == None:
		return e403
	id = request.POST["id"]
	print("Deleting", id, type(id))
	Actividad.objects.filter(id=id).delete()
	return redirect("/src/activities/activities.html")



def upload_evidence(request):
	user = get_user(request, ["Estudiante"])
	if user == None or request.method != "POST":
		return e403
	#TODO
	
