// Sports Player Hub — Global JS

// Mobile menu toggle
function toggleMenu() {
  const sidebar = document.getElementById('sidebar');
  const navLinks = document.querySelector('.nav-links');
  const navAuth = document.querySelector('.nav-auth');
  if (sidebar) {
    sidebar.classList.toggle('open');
  } else {
    // Public nav mobile toggle
    if (navLinks) navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
    if (navAuth) navAuth.style.display = navAuth.style.display === 'flex' ? 'none' : 'flex';
  }
}

// Navbar scroll effect
window.addEventListener('scroll', () => {
  const nav = document.querySelector('.navbar');
  if (nav) {
    if (window.scrollY > 60) {
      nav.style.background = 'rgba(8,12,20,0.98)';
      nav.style.boxShadow = '0 4px 24px rgba(0,0,0,0.4)';
    } else {
      nav.style.background = 'rgba(8,12,20,0.85)';
      nav.style.boxShadow = 'none';
    }
  }
});

// Animate elements on scroll
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.feature-card, .role-card, .player-card, .team-card, .tournament-card').forEach(el => {
  el.style.opacity = '0';
  el.style.transform = 'translateY(30px)';
  el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
  observer.observe(el);
});

// Sidebar active link
const sidebarItems = document.querySelectorAll('.sidebar-item');
sidebarItems.forEach(item => {
  item.addEventListener('click', function() {
    if (!this.querySelector('[style*="background:var(--red)"]')) {
      sidebarItems.forEach(i => i.classList.remove('active'));
      this.classList.add('active');
    }
  });
});

// Approve/Reject buttons
document.querySelectorAll('.btn-approve').forEach(btn => {
  btn.addEventListener('click', function() {
    const item = this.closest('.pending-item');
    const name = item.querySelector('.pending-name').textContent;
    item.style.opacity = '0';
    item.style.transform = 'translateX(20px)';
    item.style.transition = 'all .3s';
    setTimeout(() => item.remove(), 300);
    showNotif(`✅ ${name} approved successfully`);
  });
});

document.querySelectorAll('.btn-reject').forEach(btn => {
  btn.addEventListener('click', function() {
    const item = this.closest('.pending-item');
    const name = item.querySelector('.pending-name').textContent;
    item.style.opacity = '0';
    item.style.transform = 'translateX(-20px)';
    item.style.transition = 'all .3s';
    setTimeout(() => item.remove(), 300);
    showNotif(`❌ ${name} registration rejected`, true);
  });
});

function showNotif(msg, isError = false) {
  const notif = document.createElement('div');
  notif.textContent = msg;
  notif.style.cssText = `
    position:fixed;bottom:2rem;right:2rem;z-index:9999;
    background:${isError ? 'var(--red)' : 'var(--accent)'};
    color:${isError ? '#fff' : '#080c14'};
    padding:.8rem 1.5rem;border-radius:10px;
    font-weight:700;font-size:.9rem;
    animation:fadeUp .3s ease;
    box-shadow:0 8px 24px rgba(0,0,0,0.4);
  `;
  document.body.appendChild(notif);
  setTimeout(() => { notif.style.opacity='0'; notif.style.transition='opacity .3s'; setTimeout(()=>notif.remove(),300); }, 3000);
}

// Animate KPI numbers
function animateCount(el, target) {
  let start = 0;
  const duration = 1200;
  const step = (timestamp) => {
    if (!start) start = timestamp;
    const progress = Math.min((timestamp - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(eased * target);
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target;
  };
  requestAnimationFrame(step);
}

const kpiObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const val = parseInt(entry.target.textContent);
      if (!isNaN(val) && val > 10) animateCount(entry.target, val);
      kpiObserver.unobserve(entry.target);
    }
  });
});

document.querySelectorAll('.kpi-value, .stat-n').forEach(el => kpiObserver.observe(el));

console.log('🏆 Sports Player Hub loaded!');
