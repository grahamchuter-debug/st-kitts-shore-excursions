(function () {
  'use strict';

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    document.addEventListener('click', function (e) {
      if (!nav.contains(e.target) && !toggle.contains(e.target)) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  document.querySelectorAll('.faq-question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.faq-item');
      var open = item.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var name = (document.getElementById('name') || {}).value || '';
      var email = (document.getElementById('email') || {}).value || '';
      var cruise = (document.getElementById('cruise-line') || {}).value || '';
      var shipDate = (document.getElementById('ship-date') || {}).value || '';
      var topicEl = document.getElementById('topic');
      var topic = topicEl ? (topicEl.options[topicEl.selectedIndex].text || topicEl.value) : '';
      var message = (document.getElementById('message') || {}).value || '';

      var subject = 'St Kitts shore excursion enquiry';
      if (topic) subject += ' - ' + topic;

      var body = [
        'Name: ' + name,
        'Reply email: ' + email,
        'Cruise line: ' + (cruise || '(not provided)'),
        'Ship / port date: ' + (shipDate || '(not provided)'),
        'Topic: ' + (topic || '(not provided)'),
        '',
        'Message:',
        message,
        '',
        '(Sent via mailto draft from stkittsshoreexcursion.com - customer must press Send in their email app.)'
      ].join('\n');

      var mailto =
        'mailto:hello@stkittsshoreexcursion.com' +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(body);

      window.location.href = mailto;

      var msg = document.getElementById('form-success');
      if (msg) {
        msg.hidden = false;
        msg.focus();
      }
    });
  }
})();
