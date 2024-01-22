document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("backAccount").addEventListener("click", function () {
        window.location.href = "/user";
    });

    let back_predict_form = document.getElementById("backPredictForm")
    if (back_predict_form) {
        back_predict_form.addEventListener("click", function () {
            window.location.href = "/user/predict_form";
        });
    }
});