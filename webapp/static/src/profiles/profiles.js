
var select = document.createElement("select")
select.name = "rol"
select.className = "form-control"

fetch("/send_rol")
.then((response) => response.json())
.then((data) =>{
  data.forEach((x)=> {
    var option = document.createElement("option")
    option.value = x.id
    if (x.name == null){
      option.textContent = x.uname
    }else{
      option.textContent = x.name
    }
    select.appendChild(option)
  })
  console.log(select.outerHTML)
})



const tablaUsuarios = document.getElementById("tabla-usuarios");

// Función para cargar los usuarios y llenar la tabla
setTimeout( function() {
  fetch("/send_users?asd=1")
  .then((response) => response.json())
  .then((data) => {
    // Filtrar usuarios con roles "Estudiante" y "Secretaria"
    // Loop through each filtered user in the array
    var user = data
    var count = 0
    data.forEach((user) => {
      if (user.rol == 0){
        var rol = "Estudiante"
      }
      if (user.rol == 1){
        var rol = "Secretaria"
      }
      const row = document.createElement("tr");
      row.innerHTML = `
          <td>${user.uname}</td>
          <td>${user.ulname}</td>
          <td>${user.email}</td>
          <td>${rol}</td>
          <td>
              <a href="#" class="edit-button" data-bs-toggle="modal" data-bs-target="#EditModal${count}" >
                  <img src="../../assets/edit.png" alt="Editar" style="max-width: 30px;">
              </a>
              <a href="#" class="delete-button" data-bs-toggle="modal" data-bs-target="#myDeleteModal${count}">
                  <img src="../../assets/trash.png" alt="Eliminar" style="max-height: 30px;">
              </a>
          </td>

          <div class="modal text-light" id="EditModal${count}">
          <div class="modal-dialog">
        <div class="modal-content bg-dark">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Editar Usuario</h4>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <!-- Modal body -->
          <div class="modal-body">
            <form
              action="/edit_user"
              method="POST"
              id="formedit${count}"
              class="was-validated d-grid text-light">
 
            </form>
          </div>

          <!-- Modal footer -->
          <div class="modal-footer">

            <button
              type="button"
              class="btn btn-danger"
              data-bs-dismiss="modal"
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>



    <div class="modal" id="myDeleteModal${count}">
    <div class="modal-dialog">
      <div class="modal-content text-light bg-dark">
        <!-- Modal Header -->
        <div class="modal-header">
          <h4 class="modal-title">Eliminar Usuario</h4>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
          ></button>
        </div>

        <!-- Modal body -->
        <div class="modal-body">
          ¿Estás seguro que deseas eliminar el usuario ${user.uname}?
        </div>

        <!-- Modal footer -->
        <div class="modal-footer">
        <form action="/delete_username" method="post" id="formdelete${count}">
        </form>
        </div>
      </div>
    </div>
  </div>
        `;

      tablaUsuarios.appendChild(row);

      var form = document.querySelector("#formdelete" + count)

      form.innerHTML = `         
      <input type="hidden" name="id" value="${user.id}"> </input>
      <button
      type="submit"
      class="btn btn-success"
      data-bs-dismiss="modal"
      id="dmodal-aceptar">Aceptar</button>
    <button
      type="button"
      class="btn btn-danger"
      data-bs-dismiss="modal">Cerrar</button>`


      var form = document.querySelector("#formedit" + count)
      form.innerHTML = `
      <input type="hidden" name="id" value="${user.id}"> </input>
      <div>
        <div class="mb-0 mt-2">
          <label for="uname" class="form-label">Nombre:</label>
          <input
            type="text"
            class="form-control"
            id="uname"
            placeholder="Nombre"
            name="uname"
            value="${user.uname}"
            required
          />
        </div>
        <div class="mb-0 mt-2">
        <label for="ulname" class="form-label">Apellido:</label>
        <input
          type="text"
          class="form-control"
          id="uname"
          placeholder="Apellido"
          name="ulname"
          value="${user.ulname}"
          required
        />
      </div>
      <div class="mb-0 mt-2">
      <label for="email" class="form-label">Email:</label>
      <input
        type="text"
        class="form-control"
        id="email"
        placeholder="Nombre"
        name="email"
        value="${user.email}"
        required
      />
    </div>
        <div class="mb-0 mt-2">
          <label for="tipo" class="form-label">Rol:</label>  
         ${select.outerHTML}
        </div>

      </div>
       
       <button type="submit" class="btn btn-primary btn-block">Modificar</button>
      `

      count = count + 1
    });
var stype = document.querySelector("#pivot")
console.log(stype)
stype.innerHTML = select.innerHTML
  })
  .catch(console.error);

}, 800)
