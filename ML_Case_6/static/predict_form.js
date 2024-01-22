document.addEventListener("DOMContentLoaded", function () {
    let accessToken = localStorage.getItem("access_token");

    if (!accessToken) {
        window.location.href = "/";
    }

    document.getElementById("predictForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Предотвращаем отправку формы по умолчанию

        // Создаем объект FormData
        let formData = new FormData();
        formData.append("gender", document.getElementById("genderField").value);
        formData.append("race", document.getElementById("raceField").value);
        formData.append("date_birth", document.getElementById("dateBirthField").value);

        formData.append("tp53", document.getElementById("tp53").value);
        formData.append("idh1", document.getElementById("idh1").value);
        formData.append("atrx", document.getElementById("atrx").value);
        formData.append("pten", document.getElementById("pten").value);
        formData.append("egrf", document.getElementById("egrf").value);
        formData.append("cic", document.getElementById("cic").value);
        formData.append("muc16", document.getElementById("muc16").value);
        formData.append("pik3ca", document.getElementById("pik3ca").value);
        formData.append("nf1", document.getElementById("nf1").value);
        formData.append("pic3r1", document.getElementById("pic3r1").value);
        formData.append("fubp1", document.getElementById("fubp1").value);
        formData.append("rb1", document.getElementById("rb1").value);
        formData.append("notch1", document.getElementById("notch1").value);
        formData.append("bcor", document.getElementById("bcor").value);
        formData.append("csmd3", document.getElementById("csmd3").value);
        formData.append("smarca4", document.getElementById("smarca4").value);
        formData.append("grin2a", document.getElementById("grin2a").value);
        formData.append("idh2", document.getElementById("idh2").value);
        formData.append("fat4", document.getElementById("fat4").value);
        formData.append("pdgfra", document.getElementById("pdgfra").value);

        console.log("accessToken", accessToken)

        fetch("/create_diagnosis_data", {
            method: "POST",
            body: formData,
            headers: {
                "Authorization": "Bearer " + accessToken
            }
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    console.error("Ошибка:", response.statusText);
                    throw new Error("Ошибка при выполнении POST-запроса на /create_diagnosis_data");
                }
            })
            .then(data => {
                if (data.success) {
                    window.location.href = '/user/predicts'
                }
            })
            .catch(error => {
                console.error("Ошибка:", error);
            });
    });
});