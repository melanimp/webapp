const tablaUsuarios = document.getElementById("tabla-usuarios");

fetch("/send_sactivities")
  .then((response) => response.json())
  .then((data) => {
    // Loop through each user in the array
    data.act.forEach((act) => {
      var count = 0
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${act.uname}</td>
        <td>${act.type_id[0].name}</td>
        <td>${act.date}</td>
        <td>
            <form action="/subir_sactivities" method="POST" id="form${count}" enctype="multipart/form-data">
              <input type='text' value=${act.id} name="actid" style="display: none;"> </input>
              <input type='file' id="fileinput${count}" name='file'> </input>
              <button type='submit'>Subir</button>
            </form>

        </td>
      `;
      tablaUsuarios.appendChild(row);
      count = count + 1 
    });
  })
  .catch(console.error);