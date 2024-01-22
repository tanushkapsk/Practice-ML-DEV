document.addEventListener("DOMContentLoaded", function () {
    let accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        window.location.href = "/";
    }

    fetch("/get_predict", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + accessToken
        }
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                console.error("Ошибка:", response.statusText);
                throw new Error("Ошибка при выполнении GET-запроса на /get_predict");
            }
        })
        .then(data => {
            let divElement = document.createElement('div');
            divElement.innerHTML = data.rendered_template;
            let container = document.getElementById('tableContainer');
            container.appendChild(divElement);
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });
});