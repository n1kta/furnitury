const   body = document.getElementById('body'),
        modal = document.querySelector('.modal'),
        modalUser = document.getElementById('modal-user'),
        modalCart = document.getElementById('modal-cart'),
        userButton = document.getElementById('user-button'),
        cartButton = document.getElementById('cart-button'),
        modalCloseUser = document.getElementById('modal-close-user'),
        modalCloseCart = document.getElementById('modal-close-cart');

function toggleModalUser() {
    modalUser.classList.toggle('active');
    body.classList.toggle('no-scroll');  
}
function toggleModalCart() {
    modalCart.classList.toggle('active');
    body.classList.toggle('no-scroll');  
}

function closeModalCart() {
    modalCart.classList.toggle('active');
    body.classList.toggle('no-scroll');  
}
function closeModalUser() {
    modalUser.classList.toggle('active');
    body.classList.toggle('no-scroll');    
}

if (modalCloseCart) {
    modalCloseCart.addEventListener('click', closeModalCart);
}

if (modalCloseUser) {
    modalCloseUser.addEventListener('click', closeModalUser);
}

if (userButton) {
    userButton.addEventListener('click', toggleModalUser);

}
if (cartButton) {
    cartButton.addEventListener('click', toggleModalCart);

}

new WOW().init();