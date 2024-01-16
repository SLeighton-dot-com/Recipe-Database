// Wait for the webpage to load completely before running the code inside.
document.addEventListener('DOMContentLoaded', function () {
    // Find elements on the page that are used for the side menu (like a navigation drawer).
    let sidenav = document.querySelectorAll('.sidenav');
    // Set up the side menu so it works (opens and closes) correctly.
    M.Sidenav.init(sidenav, {});

    // Find dropdown menu elements on the page.
    let selects = document.querySelectorAll("select");
    // Set up the dropdown menus to look nice and work properly.
    M.FormSelect.init(selects);
});

// Find elements on the page that can be opened and closed like an accordion.
let collapsibles = document.querySelectorAll(".collapsible");
// Set up these elements so they can be opened and closed.
M.Collapsible.init(collapsibles);
