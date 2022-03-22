function formatUsername(id) {
  username = document.querySelector(id);
  username.value = username.value.replace(' ', '');
}

function openMenu(id) {
  menu = document.querySelector(id)
  menu.classList.add('is-open')
  backdrop = document.querySelector('#backdrop')
  backdrop.classList.add('is-active')
}

function closeMenu(id) {
  menu = document.querySelector(id)
  menu.classList.remove('is-open')
  backdrop = document.querySelector('#backdrop')
  backdrop.classList.remove('is-active')
}