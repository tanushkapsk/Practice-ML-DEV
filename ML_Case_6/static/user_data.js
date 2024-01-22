document.addEventListener("DOMContentLoaded", function () {
    let accessToken = localStorage.getItem("access_token");

    fetch("/get_user_data", {
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
                throw new Error("Ошибка при выполнении GET-запроса на /get_user_data");
            }
        })
        .then(data => {
            let headDiv = document.getElementById("container");
            let headButtonsDiv = document.createElement("div");
            headButtonsDiv.classList.add("buttons");

            if (data.error_key && data.error_key[0] === "not_authorization") {
                let button_authorization = document.createElement("button");
                let button_registration = document.createElement("button");
                let error_message = document.createElement("p");

                error_message.textContent = data.error_message
                button_authorization.textContent = "Авторизация";
                button_registration.textContent = "Регистрация";

                button_authorization.addEventListener("click", function () {
                    window.location.href = "/authorization";
                });

                button_registration.addEventListener("click", function () {
                    window.location.href = "/registration";
                });

                error_message.classList.add("text-error");
                button_authorization.classList.add("head-button");
                button_registration.classList.add("head-button");

                if (headButtonsDiv) {
                    headButtonsDiv.appendChild(button_authorization);
                    headButtonsDiv.appendChild(button_registration);
                }

                if (headDiv) {
                    headDiv.appendChild(error_message);
                }

            } else {
                let button_account = document.createElement("button");
                button_account.textContent = "Личный кабинет";

                button_account.addEventListener("click", function () {
                    window.location.href = "/user";
                });
                headButtonsDiv.appendChild(button_account);

                let user_name = document.getElementById("userName")
                let first_name = document.getElementById("firstName")
                let last_name = document.getElementById("lastName")
                let predict_count = document.getElementById("countPredict")
                let balance = document.getElementById("countBalance")
                let dateBirth = document.getElementById("dateBirth")
                let gender = document.getElementById("gender")
                let race = document.getElementById("race")
                let dateLastPredict = document.getElementById("dateLastPredict")
                let gradeLastPredict = document.getElementById("gradeLastPredict")

                if (user_name) {
                    user_name.textContent = data.user.username;
                }

                if (user_name) {
                    user_name.textContent = data.user.first_name;
                }

                if (first_name) {
                    first_name.textContent = data.user.first_name;
                }

                if (last_name) {
                    last_name.textContent = data.user.last_name;
                }

                if (predict_count) {
                    predict_count.textContent = data.user.predict_count;
                }

                if (balance) {
                    balance.textContent = data.user.balance;
                }

                if (dateBirth) {
                    dateBirth.textContent = data.user.date_birth
                }

                if (gender) {
                    gender.textContent = data.user.gender
                }

                if (race) {
                    race.textContent = data.user.race
                }

                if (dateLastPredict) {
                    dateLastPredict.textContent = data.user.grade_last_predict
                }

                if (gradeLastPredict) {
                    gradeLastPredict.textContent = data.user.date_last_predict
                }
            }
            if (headButtonsDiv && headDiv) {
                headDiv.appendChild(headButtonsDiv);
            }
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });

});