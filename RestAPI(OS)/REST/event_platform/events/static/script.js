// Ripple Effect for Buttons
document.querySelectorAll('.ripple-button').forEach(button => {
    button.addEventListener('click', function (e) {
        const rect = button.getBoundingClientRect();
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        ripple.style.left = `${e.clientX - rect.left}px`;
        ripple.style.top = `${e.clientY - rect.top}px`;
        button.appendChild(ripple);

        ripple.addEventListener('animationend', () => ripple.remove());
    });
});

// Pulse Effect for Buttons
document.querySelectorAll('.pulse-button').forEach(button => {
    button.addEventListener('mouseover', function () {
        const pulseCircle = document.createElement('div');
        pulseCircle.classList.add('pulse-circle');
        button.appendChild(pulseCircle);

        pulseCircle.addEventListener('animationend', () => pulseCircle.remove());
    });
});

// Dynamic Color Change on Hover
document.querySelectorAll('.color-change-button').forEach(button => {
    button.addEventListener('mouseover', function () {
        button.style.backgroundColor = '#1c7c31';
    });
    button.addEventListener('mouseleave', function () {
        button.style.backgroundColor = '#007bff';
    });
});
