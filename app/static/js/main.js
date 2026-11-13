// Modern LMS Client-Side Interactivity

document.addEventListener('DOMContentLoaded', function () {
  // 1. Initialize Bootstrap Tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // 2. Destructive Action Confirmation
  document.querySelectorAll('form[data-confirm]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      const message = form.getAttribute('data-confirm') || 'Are you sure you want to perform this action?';
      if (!confirm(message)) {
        e.preventDefault();
      }
    });
  });

  // 3. Quiz Countdown Timer
  const timerElement = document.getElementById('quiz-timer');
  const quizForm = document.getElementById('quiz-form');

  if (timerElement && quizForm) {
    const totalMinutes = parseInt(timerElement.getAttribute('data-minutes') || '15', 10);
    let secondsRemaining = totalMinutes * 60;

    const updateTimerDisplay = () => {
      const minutes = Math.floor(secondsRemaining / 60);
      const seconds = secondsRemaining % 60;
      timerElement.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

      if (secondsRemaining <= 120) {
        timerElement.classList.remove('bg-primary');
        timerElement.classList.add('bg-danger');
      }

      if (secondsRemaining <= 0) {
        clearInterval(timerInterval);
        alert('Time has expired! Your quiz attempt is now being automatically submitted.');
        quizForm.submit();
      }
      secondsRemaining--;
    };

    updateTimerDisplay();
    const timerInterval = setInterval(updateTimerDisplay, 1000);
  }

  // 4. Interactive Course Card Wishlist Toggle
  document.querySelectorAll('.course-card-wishlist-btn[data-course-id]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      const courseId = this.getAttribute('data-course-id');
      const csrfMeta = document.querySelector('meta[name="csrf-token"]');
      const csrfToken = csrfMeta ? csrfMeta.getAttribute('content') : '';
      const icon = this.querySelector('i');

      fetch(`/learning/wishlist/toggle/${courseId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          if (data.wishlisted) {
            btn.classList.add('active');
            if (icon) {
              icon.className = 'bi bi-heart-fill text-danger';
            }
            btn.setAttribute('title', 'Remove from Wishlist');
          } else {
            btn.classList.remove('active');
            if (icon) {
              icon.className = 'bi bi-heart';
            }
            btn.setAttribute('title', 'Save to Wishlist');
          }

          // Update navbar wishlist badge counters in real time
          document.querySelectorAll('.badge-counter-wishlist').forEach(function (badge) {
            let currentCount = parseInt(badge.textContent.trim(), 10) || 0;
            currentCount = data.wishlisted ? currentCount + 1 : Math.max(0, currentCount - 1);
            badge.textContent = currentCount;
            badge.style.display = currentCount > 0 ? '' : 'none';
          });
        }
      })
      .catch(err => {
        console.error('Wishlist toggle error:', err);
      });
    });
  });
});
