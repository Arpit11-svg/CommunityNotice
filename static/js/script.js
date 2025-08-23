console.log('Community Notice Board Template Loaded');
// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
  const dropdown = document.querySelector('.profile-dropdown');
  if (!dropdown) return;

  dropdown.addEventListener('click', e => {
    e.stopPropagation();
    dropdown.classList.toggle('open');
  });

  // close if clicked outside
  document.addEventListener('click', () => {
    dropdown.classList.remove('open');
  });
});
