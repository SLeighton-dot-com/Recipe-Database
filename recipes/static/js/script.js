document.addEventListener('DOMContentLoaded', function () {
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav, {});
});

let collapsibles = document.querySelectorAll(".collapsible");
M.Collapsible.init(collapsibles);
