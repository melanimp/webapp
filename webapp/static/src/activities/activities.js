const tablaUsuarios = document.getElementById("tabla-usuarios");

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
var select = document.createElement("select")
select.name = "type"
select.className = "form-control"

var label = document.querySelector("#pivot")
label.insertAdjacentElement("afterend", select)

fetch("/send_type")
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
setTimeout( function() {
fetch("/send_sactivities")
  .then((response) => response.json())
  .then((data) => {
    // Loop through each user in the array

    var count = 0
    data.act.forEach((act) => {
      
      console.log(count)
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${act.uname}</td>
        <td>${act.type_id[0].name}</td>
        <td>${act.date}</td>
        <td>
            <a href="" data-bs-toggle="modal" data-bs-target="#myEditModal${count}">
                <img src="../../assets/edit.png" alt="Editar" style="max-width: 30px;">
            </a>
            <a href="" class="mx-2" data-bs-toggle="modal" data-bs-target="#myDeleteModal${count}">
                <img src="../../assets/trash.png" alt="Eliminar" style="max-height: 30px;">
            </a>
            <div class="modal text-light" id="myEditModal${count}">
      <div class="modal-dialog">
        <div class="modal-content bg-dark">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Editar Actividad</h4>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <!-- Modal body -->
          <div class="modal-body">
            <form
              action="/edit_sactivities"
              method="POST"
              id="loginForm"
              class="was-validated d-grid text-light">
              <input type="hidden" name="id" value="${act.id}"> </input>
              <div>
                <div class="mb-0 mt-2">
                  <label for="uname" class="form-label">Nombre:</label>
                  <input
                    type="text"
                    class="form-control"
                    id="uname"
                    placeholder="Nombre"
                    name="uname"
                    value="${act.uname}"
                    required
                  />
                </div>
                <div class="mb-0 mt-2">
                  <label for="tipo" class="form-label">Tipo:</label>  
                 ${select.outerHTML}
                </div>
                <div class="mb-0 mt-2 text-light">
                  <label for="email" class="form-label">Fecha:</label>
                  <input
                    type="date"
                    class="form-control"
                    id="fecha"
                    placeholder="Fecha"
                    value="${act.date}"
                    name="date"
                  />
                </div>
              </div>
               
               <button type="submit" class="btn btn-primary btn-block">Modificar</button>
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
            <h4 class="modal-title">Eliminar Actividad</h4>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <!-- Modal body -->
          <div class="modal-body">
            ¿Estás seguro que deseas eliminar <b>"${act.uname}"</b>?
          </div>

          <!-- Modal footer -->
          <div class="modal-footer">
          <form action="/ractivities" method="POST">
            <input type="hidden" name="id" value="${act.id}"> </input>
            <button
              type="submit"
              class="btn btn-success"
              data-bs-dismiss="modal"
              id="dmodal-aceptar"
            >
              Aceptar
            </button>
            <button
              type="button"
              class="btn btn-danger"
              data-bs-dismiss="modal"
            >
              Cerrar
            </button>
          </form>
          </div>
        </div>
      </div>
    </div>

        </td>
      `;
      count =  count + 1
      tablaUsuarios.appendChild(row);
    });
  })
  .catch(console.error);

}, 800)