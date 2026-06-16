/* ============================================================
   MAIN.JS — Scripts globais do site RD Webdesign
   ============================================================ */

/* ---------- Navegação: efeito ao rolar a página ---------- */
const nav = document.querySelector('nav');
window.addEventListener('scroll', () => {
  nav?.classList.toggle('scrolled', window.scrollY > 40);
});

/* ---------- Menu hamburguer (mobile) ---------- */
const toggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');

toggle?.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

// Fecha o menu ao clicar em um link
navLinks?.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => navLinks.classList.remove('open'));
});

/* ---------- Animação de entrada dos elementos (scroll) ---------- */
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target); // Anima só uma vez
      }
    });
  },
  { threshold: 0.12 }
);

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

/* ---------- Formulário de contato: abre WhatsApp com os dados ---------- */
const form = document.querySelector('.contact-form');
const btnSubmit = document.querySelector('.btn-submit');

btnSubmit?.addEventListener('click', (e) => {
  e.preventDefault();

  const nome    = document.querySelector('[name="nome"]')?.value.trim();
  const servico = document.querySelector('[name="servico"]')?.value;
  const mensagem = document.querySelector('[name="mensagem"]')?.value.trim();

  // Monta a mensagem para o WhatsApp
  let texto = 'Olá! Vim pelo site da RD Webdesign e gostaria de um orçamento.';
  if (nome)    texto += `\n\n*Nome:* ${nome}`;
  if (servico) texto += `\n*Serviço:* ${servico}`;
  if (mensagem) texto += `\n*Mensagem:* ${mensagem}`;

  window.open(`https://wa.me/5511996523787?text=${encodeURIComponent(texto)}`, '_blank');
});

/* ---------- Tabs na página de serviços (se existir) ---------- */
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.tab;

    // Remove active de todos
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

    // Ativa o clicado
    btn.classList.add('active');
    document.querySelector(`[data-panel="${target}"]`)?.classList.add('active');
  });
});

/* ---------- Contagem animada dos números no hero ---------- */
function animateCount(el) {
  const target = parseInt(el.dataset.count);
  const duration = 1500;
  const step = target / (duration / 16);
  let current = 0;

  const timer = setInterval(() => {
    current += step;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    el.textContent = Math.floor(current);
  }, 16);
}

// Inicia contagem quando os stats aparecem na tela
const statsObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('[data-count]').forEach(animateCount);
      statsObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

document.querySelector('.hero-stats') && statsObserver.observe(document.querySelector('.hero-stats'));
