 fetch("/asistencia")
      .then((response) => response.json())
      .then((estudiantes) => {       
        const tablaUsuarios = document.getElementById("tabla-usuarios");
        estudiantes.forEach((estudiante) => {
          const row = document.createElement("tr");
          row.innerHTML = `
          <td>${estudiante.event}</td>
          <td>${estudiante.uname}</td>
            <td>${estudiante.ulname}</td>
            <td>${estudiante.att}</td>
          `;
          tablaUsuarios.appendChild(row);
        });
      })
 