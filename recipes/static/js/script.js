document.addEventListener('DOMContentLoaded', function () {
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav, {});

    let selects = document.querySelectorAll("select");
    M.FormSelect.init(selects);
});

let collapsibles = document.querySelectorAll(".collapsible");
M.Collapsible.init(collapsibles);
