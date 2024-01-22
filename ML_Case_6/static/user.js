document.addEventListener("DOMContentLoaded", function () {
    let accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        window.location.href = "/";
    }

    document.getElementById("predictsList").addEventListener("click", function () {
        window.location.href = "/user/predicts";
    });

    document.getElementById("predictForm").addEventListener("click", function () {
        window.location.href = "/user/predict_form";
    });

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
            if (data.user.predict_count === 0) {
                let predict_button = document.getElementById("predictsList")
                predict_button.disabled = true;
                predict_button.style.pointerEvents = "none";
                predict_button.style.backgroundColor = "#555555";
                predict_button.style.color = "white";
            }

            if (data.user.balance < 100) {
                let predict_form_button = document.getElementById("predictForm")
                predict_form_button.disabled = true;
                predict_form_button.style.pointerEvents = "none";
                predict_form_button.style.backgroundColor = "#555555";
                predict_form_button.style.color = "white";
            }

            document.getElementById("userName").textContent = data.user.username;
            document.getElementById("firstName").textContent = data.user.first_name;
            document.getElementById("lastName").textContent = data.user.last_name;
            document.getElementById("dateBirth").textContent = data.user.date_birth;
            document.getElementById("gender").textContent = data.user.gender;
            document.getElementById("race").textContent = data.user.race;
            document.getElementById("gradeLastPredict").textContent = data.user.grade_last_predict;
            document.getElementById("dateLastPredict").textContent = data.user.date_last_predict;
            document.getElementById("countPredict").textContent = data.user.predict_count;
            document.getElementById("countBalance").textContent = data.user.balance;
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });
});