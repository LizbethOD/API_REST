function getClientes() {
    
    var request = new XMLHttpRequest(); //Accede a la session de la pagina
   
    username= prompt("username");
    password= prompt("password");
    

    request.open('GET', "https://8000-lizbethod-apirest-h5fixnrf1oq.ws-us54.gitpod.io/clientes/");
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Authorization", "Basic " + btoa(username + ":" + password))
    request.setRequestHeader("content-Type", "application/json");
    
    const  tabla   = document.getElementById("clientes_Table");  
   
    var tblBody = document.createElement("tbody");
    var tblHead = document.createElement("thead");
    
    tblHead.innerHTML = `
        <tr>
            <th>ID</th>
            <th>NOMBRE</th>
            <th>EMAIL</th>
            <th>DETALLE</th>
            <th>ACTUALIZAR</th>
            <th>ELIMINAR</th>
        </tr>`;
   
    request.onload = () => {
            // Almacena la respuesta en una variable, si es 202 es que se obtuvo correctamente
            const response = request.responseText;
            const json = JSON.parse(response);
            
            if (request.status === 401 || request.status === 403) {
                alert(json.detail);
            }
            else if (request.status == 202){
                const response = request.responseText;
                const json = JSON.parse(response);
                for (let a = 0; a < json.length; a++) {
                    var tr = document.createElement('tr');
                    var id_cliente = document.createElement('td');
                    var nombre = document.createElement('td');
                    var email = document.createElement('td');
                    var detalle = document.createElement('td');
                    var actualizar = document.createElement('td');
                    var eliminar = document.createElement('td');
                    
                    id_cliente.innerHTML = json[a].id_cliente;
                    nombre.innerHTML = json[a].nombre;
                    email.innerHTML = json[a].email;
                    detalle.innerHTML = "<a href='/templetes/get_cliente.html?"+json[a].id_cliente+ "'>Detalle</a>";
                    actualizar.innerHTML = "<a href='/templetes/put_cliente.html?"+json[a].id_cliente+ "'>Actualizar</a>";
                    eliminar.innerHTML = "<a href='/templetes/delete_cliente.html?"+json[a].id_cliente+ "'>Eliminar</a>";

                    tr.appendChild(id_cliente);
                    tr.appendChild(nombre);
                    tr.appendChild(email);
                    tr.appendChild(detalle);
                    tr.appendChild(actualizar);
                    tr.appendChild(eliminar);
                    
                    tblBody.appendChild(tr);
                }
                tabla.appendChild(tblHead);
                tabla.appendChild(tblBody);
        }    
    };
    request.send();
};