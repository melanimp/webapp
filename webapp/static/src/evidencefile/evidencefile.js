const tablaUsuarios = document.getElementById("tabla-usuarios");

fetch("/send_evidence")
  .then((response) => response.json())
  .then((data) => {
    // Loop through each user in the array
    data.evd.forEach((evd) => {
      var asd = ""
      if (evd.att == true){
        asd = "Si"
      }else{
        asd = "No"
      }
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${evd.event_id}</td>
        <td>${evd.uname_id}</td>
        <td>${asd}</td>
        <td>${evd.recog}</td>
        <td>
            <a href="${evd.doc}" class="d-flex align-items-center text-decoration-none text-light" >
                <img src="../../assets/download.png" alt="Editar" class="mr-2" style="max-width: 30px;">
                <h1 class="display-6 align-self-center mx-1 mt-1" style="font-size: 20px;">archivo</h1>
            </a>
        </td>
      `;
      tablaUsuarios.appendChild(row);
    });
  })
  .catch(console.error);