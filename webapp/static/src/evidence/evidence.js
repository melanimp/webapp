const tablaUsuarios = document.getElementById("tabla-usuarios");
var asistencia

function asd(url, pivot){
  var select = document.createElement("select")
  select.name = "type" + pivot.slice(1,)
  select.className = "form-control"

  var label = document.querySelector(pivot)
  label.insertAdjacentElement("afterend", select)

  fetch(url)
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
}

asd("/send_users", "#pivotusername")
asd("/send_activities", "#pivotactividad")

fetch("/send_evidence")
  .then((response) => response.json())
  .then((data) => {
    // Loop through each user in the array
    var count = 0
    data.evd.forEach((evd) => {
      if (evd.att != true){
        asistencia = "No"
      }else{
        asistencia = "Si"
      }
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${evd.event_id}</td>
        <td>${evd.uname_id}</td>
        <td>${asistencia}</td>
        <td>${evd.recog}</td>
        <td>
            <a href="${evd.doc}" class="d-flex align-items-center text-decoration-none text-light" >
                Descargar
            </a>
        </td>
        <td>

            <a href="" data-bs-toggle="modal" data-bs-target="#Modal${count}">
                <img src="../../assets/edit.png" alt="Editar" style="max-width: 30px;">
            </a>

            <a href="" class="mx-2" data-bs-toggle="modal" data-bs-target="#myDeleteModal${count}">
                <img src="../../assets/trash.png" alt="Eliminar" style="max-height: 30px;">
            </a>
        </td>
        <div class="modal text-light" id="Modal${count}">
      <div class="modal-dialog">
        <div class="modal-content bg-dark">
          <!-- Modal Header -->
          <div class="modal-header">
            <h4 class="modal-title">Editar Evidencia</h4>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
            ></button>
          </div>

          <!-- Modal body -->
          <div class="modal-body">
          <form action="/edit_evidence" method="post" id="formedit${count}">
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
          <h4 class="modal-title">Eliminar Evidencia</h4>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
          ></button>
        </div>

        <!-- Modal body -->
        <div class="modal-body">
          ¿Estás seguro que deseas eliminar la evidencia?
        </div>

        <!-- Modal footer -->
        <div class="modal-footer">
        <form action="/delete_evidence" method="post" id="formdelete${count}" >
        </form>
        </div>
      </div>
    </div>
  </div>
      `;
      tablaUsuarios.appendChild(row);
      var form = document.querySelector("#formedit" + count)
      form.innerHTML = `
      <input type="hidden" name="id" value="${evd.id}"> </input>
      <label class="form-label">Reconocimiento:</label>
      <input type="text" class="form-control" placeholder="Reconocimiento" name="recog" value="${evd.recog}" required />
      <button type="submit" class="btn btn-primary btn-block">Modificar</button>
      `
      var form = document.querySelector("#formdelete" + count)

      form.innerHTML = `         
      <input type="hidden" name="id" value="${evd.id}"> </input>
      <button
      type="submit"
      class="btn btn-success"
      data-bs-dismiss="modal"
      id="dmodal-aceptar">Aceptar</button>
    <button
      type="button"
      class="btn btn-danger"
      data-bs-dismiss="modal">Cerrar</button>`
      count = count + 1
    });
  })
  .catch(console.error);