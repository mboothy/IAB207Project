let subMenu = document.getElementById("subMenu");
function toggleMenu() {
    subMenu.classList.toggle("open-menu");
}
let alert = document.getElementById("alertid");
function closealert() {
    alert.classList.toggle("closealert");
}
let logout_message = document.getElementById("logout_messageid");
function show_log_out_message() {
    logout_message.classList.toggle("show");
    setTimeout(() =>  logout_message.classList.toggle("show"), 5000)
}

setTimeout(alert.classList.add("hidden"),5000);