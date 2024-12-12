const toggleButton = document.getElementById("toggle-menu");
const menuItems = document.getElementById("menu-items");

toggleButton.addEventListener("click", () => {
    menuItems.classList.toggle("active");
    toggleButton.classList.toggle("active");
});
