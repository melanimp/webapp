const tablaUsuarios = document.getElementById("tabla-usuarios");

// Función para cargar los usuarios y llenar la tabla
function cargarUsuarios() {
  fetch("../users.json")
    .then((response) => response.json())
    .then((data) => {
      tablaUsuarios.innerHTML = ""; // Limpiar la tabla antes de volver a llenarla

      // Loop through each user in the array
      data.users.forEach((user) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${user.uname}</td>
          <td>${user.ulname}</td>
          <td>${user.pass}</td>
          <td>${user.email}</td>
          <td>${user.rol}</td>
          <td>
              <a href="#" class="edit-button" data-bs-toggle="modal" data-bs-target="#myEditModal">
                  <img src="../../assets/edit.png" alt="Editar" style="max-width: 30px;">
              </a>
              <a href="#" class="delete-button" data-bs-toggle="modal" data-bs-target="#myDeleteModal">
                  <img src="../../assets/trash.png" alt="Eliminar" style="max-height: 30px;">
              </a>
          </td>
        `;

        // Agregar evento de clic al botón de eliminar
        const deleteButton = row.querySelector(".delete-button");
        deleteButton.addEventListener("click", function () {
          handleDeleteUser(user.uname);
        });

        tablaUsuarios.appendChild(row);
      });
    })
    .catch(console.error);
}

// Función para eliminar un usuario por su nombre de usuario y todos sus datos
function deleteUserByUsername(data, username) {
  data.users = data.users.filter(function (user) {
    return user.uname !== username;
  });
}

// Función para cargar el JSON externo y manejar la eliminación de usuario al hacer clic en el botón
function handleDeleteUser(username) {
  fetch("../users.json")
    .then((response) => response.json())
    .then((data) => {
      // Eliminar el usuario con nombre de usuario 'Juan' y todos sus datos
      deleteUserByUsername(data, username);
      console.log(data)

      // Mostrar el JSON actualizado sin el usuario eliminado
      cargarUsuarios();
    })
    .catch((error) => console.error("Error al cargar el archivo JSON:", error));
}

cargarUsuarios();