const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");
const myButton = document.getElementById("button");

menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
})

closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
})

themeToggler.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme-variables');

    themeToggler.querySelector('i:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('i:nth-child(2)').classList.toggle('active');
})

// document.addEventListener(document).ready(function() {
//     document.addEventListener('a').click(function() {
//         document.addEventListener('a.onclick.active').removeClass("active");
//         document.addEventListener(this).addClass("active");
//     });
// });

// myButton.addEventListener('click', () => {
//     myButton.classList.add("active");

// })`

if (localStorage.getItem("active")) {
    //remove active
    for(let j = 0; j < elements.length; j++) {
        elements[j].classList.remove("active");
    }
    //add active
    document.getElementById(localStorage.getItem("active")).className += " active";
}
