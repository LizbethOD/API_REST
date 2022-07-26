function crearUsuario(){
    
    var email = document.getElementById("email");
    var password = document.getElementById("password");
    var d = {
        "email": email.value,
        "password": password.value
    }

    var request = new XMLHttpRequest();
    request.open("POST", "https://8000-lizbethod-apirest-52babcwb66f.ws-us54.gitpod.io/users/", true);
    request.setRequestHeader("Accept", "application/json");
    request.setRequestHeader("Content-Type", "application/json");

    request.onload = () => {
        
        const response = request.responseText;
        const json = JSON.parse(response);
        
        if (request.status == 403  ) {
            alert(json.detail);
        }
        if(request.status == 401 ){
            swal("Ya existe"); 
        }
        if (request.status == 202){
            const response = request.responseText;
            const json = JSON.parse(response);

            if (request.status == 202){
                alert("Usuario agregado exitosamente");
                window.location = "/templates/";
            }
        }
    };
    request.send(JSON.stringify(d));
};