function login(){
    
    var email = document.getElementById("email");
    var password = document.getElementById("password");

        var request = new XMLHttpRequest();
        request.open("GET", "https://8000-lizbethod-apirest-52babcwb66f.ws-us60.gitpod.io/user/validate/", true);
        request.setRequestHeader("Accept", "application/json");
        request.setRequestHeader("Authorization", "Basic " + btoa(email.value + ":" + password.value));
        request.setRequestHeader("Content-Type", "application/json");

        request.onload = () => {

            const response = request.responseText;
            const json = JSON.parse(response);

            if (request.status == 401 || request.status == 403  ) {
                alert(json.detail);
            }
            if (request.status == 202){
                const response = request.responseText;
                const json = JSON.parse(response);

                if (request.status == 202){
                    sessionStorage.setItem("token", json.token);
                    mensaje = "Hola, bienvendid@: " + email.value;
                    alert(mensaje);
                    window.location = "/templates/get_clientes.html";
                }
            }
        };
        request.send();
};