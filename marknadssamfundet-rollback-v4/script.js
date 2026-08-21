const menuBtn=document.querySelector('.menu-toggle');const nav=document.querySelector('#main-nav');if(menuBtn&&nav){menuBtn.addEventListener('click',()=>{const isOpen=nav.classList.toggle('open');menuBtn.setAttribute('aria-expanded',String(isOpen));});}
const search=document.querySelector('#search');const filters=[...document.querySelectorAll('.filter')];const items=[...document.querySelectorAll('.archive-item')];const noResults=document.querySelector('#no-results');let current='alla';function applyArchive(){if(!items.length)return;const q=(search?.value||'').toLocaleLowerCase('sv');let count=0;items.forEach(item=>{const text=((item.dataset.search||'')+' '+item.innerText).toLocaleLowerCase('sv');const okType=current==='alla'||item.dataset.type===current;const okQ=text.includes(q);item.hidden=!(okType&&okQ);if(okType&&okQ)count++;});if(noResults)noResults.hidden=count!==0;}search?.addEventListener('input',applyArchive);filters.forEach(btn=>btn.addEventListener('click',()=>{filters.forEach(b=>b.classList.remove('active'));btn.classList.add('active');current=btn.dataset.filter;applyArchive();}));const params=new URLSearchParams(location.search);if(search&&params.get('q')){search.value=params.get('q');applyArchive();}


// Version 3: mjuka scroll-animationer och sidomeny.
document.documentElement.classList.add('js-ready');

const revealSelectors = [
  '.lead-story',
  '.side-story',
  '.section-head',
  '.latest-item',
  '.editorial-box',
  '.report-card',
  '.opinion-card',
  '.archive-item',
  '.search-box',
  '.article-header',
  '.article-body',
  '.related',
  '.about-header',
  '.shop-header',
  '.principle',
  '.shop-card'
];

const revealElements = [...document.querySelectorAll(revealSelectors.join(','))];
revealElements.forEach((el, index) => {
  el.classList.add('reveal', `reveal-delay-${index % 4}`);
});

if ('IntersectionObserver' in window) {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -35px 0px' });

  revealElements.forEach(el => revealObserver.observe(el));
} else {
  revealElements.forEach(el => el.classList.add('is-visible'));
}

// Bygg en kompakt sidoflik från den befintliga huvudmenyn.
const masthead = document.querySelector('.masthead');
const mainNavLinks = [...document.querySelectorAll('#main-nav a')];

if (masthead && mainNavLinks.length) {
  const rail = document.createElement('aside');
  rail.className = 'side-rail';
  rail.setAttribute('aria-label', 'Snabbnavigering');

  const brand = document.createElement('div');
  brand.className = 'side-rail-brand';
  brand.innerHTML = '<img src="assets/mark-icon.png" alt=""><span>MARKNADSSAMFUNDET</span>';
  rail.appendChild(brand);

  const railNav = document.createElement('nav');

  mainNavLinks.forEach(link => {
    const a = document.createElement('a');
    a.href = link.href;
    if (link.classList.contains('active')) a.classList.add('active');

    const short = document.createElement('span');
    short.className = 'rail-short';
    short.textContent = link.textContent.trim().charAt(0).toUpperCase();

    const label = document.createElement('span');
    label.className = 'rail-label';
    label.textContent = link.textContent.trim();

    a.append(short, label);
    railNav.appendChild(a);
  });

  rail.appendChild(railNav);
  document.body.appendChild(rail);

  const updateRail = () => {
    const mastheadBottom = masthead.getBoundingClientRect().bottom;
    rail.classList.toggle('visible', mastheadBottom < 0);
  };

  updateRail();
  window.addEventListener('scroll', updateRail, { passive: true });
  window.addEventListener('resize', updateRail);
}
