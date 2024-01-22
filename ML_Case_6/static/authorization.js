document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("loginForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Предотвращаем отправку формы по умолчанию

        // Создаем объект FormData
        let formData = new FormData();
        formData.append("username", document.getElementById("username").value);
        formData.append("password", document.getElementById("password").value);

        // Отправляем POST-запрос на /login
        fetch("/login", {
            method: "POST",
            body: formData
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    console.error("Ошибка:", response.statusText);
                    throw new Error("Ошибка при выполнении POST-запроса на /login");
                }
            })
            .then(data => {
                if (!data.access_token || (data.error && data.error[0] === 'error_key')) {
                    let headDiv = document.getElementById("error-message");
                    let error_message = document.createElement("p");
                    error_message.textContent = data.error_message
                    error_message.classList.add("text-error-text");

                    let button_registration = document.createElement("button");
                    button_registration.textContent = "Регистрация";
                    button_registration.classList.add("button")
                    button_registration.addEventListener("click", function () {
                        window.location.href = "/registration";
                    });

                    headDiv.appendChild(error_message);
                    headDiv.appendChild(button_registration);
                } else {
                    const accessToken = data.access_token;
                    localStorage.setItem('access_token', accessToken)

                    fetch("/user", {
                        method: "GET",
                        headers: {
                            "Authorization": "Bearer " + accessToken
                        }
                    })
                        .then(response => {
                            if (response.ok) {
                                window.location.href = "/user";
                            }
                        })
                        .catch(error => {
                            console.error("Ошибка:", error);
                        });
                }
            })
            .catch(error => {
                console.error("Ошибка:", error);
            });
    });
});