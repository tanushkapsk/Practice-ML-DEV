document.addEventListener("DOMContentLoaded", function () {
    let logoutBtn = document.getElementById("logout");

    logoutBtn.addEventListener("click", function () {
        localStorage.removeItem("access_token");
        window.location.href = "/";
    });
});