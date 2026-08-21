const menuButton = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');

if (menuButton && nav) {
  menuButton.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(open));
  });
}

const searchInput = document.querySelector('#search');
const filterButtons = document.querySelectorAll('.filter');
const archiveItems = document.querySelectorAll('.archive-item');
const noResults = document.querySelector('#no-results');
let activeFilter = 'alla';

function updateArchive() {
  if (!archiveItems.length) return;
  const query = (searchInput?.value || '').toLocaleLowerCase('sv');
  let visible = 0;

  archiveItems.forEach(item => {
    const matchesFilter = activeFilter === 'alla' || item.dataset.type === activeFilter;
    const haystack = (item.dataset.search + ' ' + item.innerText).toLocaleLowerCase('sv');
    const matchesQuery = haystack.includes(query);
    const show = matchesFilter && matchesQuery;
    item.hidden = !show;
    if (show) visible++;
  });

  if (noResults) noResults.hidden = visible !== 0;
}

searchInput?.addEventListener('input', updateArchive);

filterButtons.forEach(button => {
  button.addEventListener('click', () => {
    filterButtons.forEach(b => b.classList.remove('active'));
    button.classList.add('active');
    activeFilter = button.dataset.filter;
    updateArchive();
  });
});

const params = new URLSearchParams(window.location.search);
if (searchInput && params.get('q')) {
  searchInput.value = params.get('q');
  updateArchive();
}
