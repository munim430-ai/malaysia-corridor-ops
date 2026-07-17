// Malaysia Corridor Ops — Minimal JS

// FAQ Accordion
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.faq-q').forEach(function(btn) {
    btn.addEventListener('click', function() {
      this.classList.toggle('active');
      var answer = this.nextElementSibling;
      answer.classList.toggle('open');
    });
  });
});

// GoatCounter Analytics
window.goatcounter = { path: function(p) { return location.host + p; } };
(function() {
  var gc = document.createElement('script');
  gc.async = true;
  gc.src = '//gc.zgo.at/count.js';
  gc.setAttribute('data-goatcounter', 'https://malaysia-corridor-ops.goatcounter.com/count');
  document.head.appendChild(gc);
})();
