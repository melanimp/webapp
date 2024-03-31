//Funcion con expresion regular para validar campo de nombre y apellido
function validarNombreYApellido(nombre) {
    const regexNombre = /^[a-zA-Z\s]*$/; // Expresión regular que permite solo letras y espacios
    return regexNombre.test(nombre); // Devuelve true si el nombre es válido, false si no lo es
  }
  