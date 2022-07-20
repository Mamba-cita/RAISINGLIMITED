console.log(' Mamba-cita ..............nav.js');

let navbar = document.querySelector('.navbar');
let searchBox = document.querySelector('.search-box .bx-search');



searchBox.addEventListener('click', () => {
    navbar.classList.toggle('showActive');
    if(navbar.classList.contains('showActive')){
        searchBox.classList.replace('bx-search', 'bx-x');
    }else{
        searchBox.classList.replace('bx-x', 'bx-search');
    }
}
);

//sidebar open/close
let sidebarOpen = document.querySelector('.navbar .bx-menu');
let navLinks = document.querySelector('.nav-links ');
let sidebarClose = document.querySelector('.nav-links .bx-x ');


//function to open sidebar

sidebarOpen.addEventListener('click', () => {
    navLinks.style.left = '0';

}
);
sidebarClose.addEventListener('click', () => {
    navLinks.style.left = '-100%';

}
);