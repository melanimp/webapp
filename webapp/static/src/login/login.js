var form = document.getElementById("loginForm")
var cookie = document.cookie
var cookie_list = cookie.split('=')
var csrf = ""
if (cookie_list.length > 0){
  for (var i = 0; i < cookie_list.length; i = i + 2){
    if (cookie_list[i] == "csrftoken"){
        csrf = cookie_list[i + 1]
        break
    }
  }
}

var input = document.createElement('input');
input.type = 'hidden';
input.name = 'csrfmiddlewaretoken';
input.value = csrf;


form.appendChild(input)
/*
document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Evita que el formulario se envíe automáticamente

    let email = document.getElementById("email");
    let password = document.getElementById("pwd");

    fetch("../users.json")
      .then((response) => response.json())
      .then((data) => {
        let users = data.users;

        let user = users.find(
          (user) => user.email === email.value && user.pass === password.value
        );

        if (user) {
          // Redirigir a diferentes páginas según el rol
          if (user.rol === "Administrador") {
            window.location.href = "../admin/admin.html";
          } else if (user.rol === "Secretaria") {
            window.location.href = "../evidencefile/evidencefile.html";
          } else if (user.rol === "Estudiante") {
            window.location.href = "../myevidence/myevidence.html";
          }else if (user.rol === "Jefe Año") {
            window.location.href = "../principal/principal.html";
          }
        } else {
          alert("Inicio de sesión fallido. Usuario o contraseña incorrectos.");
        }
      })
      .catch((error) =>
        console.error("Error al cargar el archivo JSON:", error)
      );
  });
*/