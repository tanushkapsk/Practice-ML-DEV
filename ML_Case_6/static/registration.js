document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("RegisterForm").addEventListener("submit", function (event) {
        event.preventDefault();

        let formData = new FormData();
        formData.append("username", document.getElementById("username").value);
        formData.append("password", document.getElementById("password").value);
        formData.append("first_name", document.getElementById("first_name").value);
        formData.append("last_name", document.getElementById("last_name").value);
        formData.append("date_birth", document.getElementById("date_birth").value);
        formData.append("gender", document.getElementById("gender").value);
        formData.append("race", document.getElementById("race").value);

        fetch("/register", {
            method: "POST",
            body: formData
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    console.error("Ошибка:", response.statusText);
                    document.getElementById("error_message").textContent = "Ошибка регистрации. Проверьте, заполнили ли вы все поля правильно.";
                }
            })
            .then(data => {
                if (data.success && data.success === true) {
                    window.location.href = "/authorization"
                }
                else {
                    document.getElementById("error_message").textContent = data.error_message
                }
            });
    });
});