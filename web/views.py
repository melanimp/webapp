from django.shortcuts import render, HttpResponse
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.middleware.csrf import get_token
import os
from web.models import Usuario



EXTENSIONS = {
    "css":"text/css",
	"map":"text/css",
    "js":"text/javascript",
	"json":"application/json",
    "html":"text/html",
    "jpg":"image/*",
    "jpeg":"image/*",
    "png":"image/*",
    "ico":"image/*",
    }

def get_user(request, rol):
	auth_token = request.COOKIES.get("auth_token")
	user = Usuario.objects.filter(auth_token=auth_token)
	if len(user) == 0:
		return None
	else:
		if user[0].rol.name in rol:
			#if os.path.dirname(request.path) in user[0].rol.path:
			return user[0]
		else:
			return None


# Create your views here.
def e404():
	return HttpResponseNotFound("404")
def e403():
	return HttpResponseForbidden("403")


def handler(request,path=""):
	ROOT="./webapp/static/"
	if path == "":
		path = "index.html"
	file = os.path.basename(path)
	if not '.' in file:
		return e404()
	ext = EXTENSIONS[file.split('.')[-1]]
	try:
		if "webapp/static" in path:
			path = path.split("webapp/static")[-1]
		content = open(ROOT+path, "rb").read()
	except FileNotFoundError:
		return e404()
	http =  HttpResponse(content,content_type=ext)
	if ext == EXTENSIONS['html']:
		if not path in ["index.html", "src/login/login.html"]:
			user = get_user(request, ["Estudiante", "Secretaria", "Jefe Año"])
			if user == None:
				return e403()
		csrf = get_token(request)
		http.set_cookie("csrftoken", csrf)
	return http