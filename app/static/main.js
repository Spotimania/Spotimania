//Menu toggle for small devices
var selectElement = function (element) {
  return document.querySelector(element);
};

var menuToggler = selectElement('.menu-toggle');
var body = selectElement('body');

menuToggler.addEventListener('click', function () {
  body.classList.toggle('open');
});

//scroll sticky navbar

// When the user scrolls the page, execute myFunction 
window.onscroll = function () { myFunction() };

// Get the navbar
var navbar = document.getElementById("top");

// Get the offset position of the navbar
var sticky = navbar.offsetTop;

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {
  if (window.pageYOffset >= sticky) {
    navbar.classList.add("sticky");
  } else {
    navbar.classList.remove("sticky");
  }
};
