document.addEventListener('DOMContentLoaded', () => {
    const showEmailFormButton = document.getElementById('show-email-form');
    const emailForm = document.getElementById('email-form');
    const buttonGroup = document.querySelector('.button-group');

    if (showEmailFormButton && emailForm) {
        showEmailFormButton.addEventListener('click', (e) => {
            e.preventDefault();
            emailForm.style.display = 'block';
            showEmailFormButton.style.display = 'none';
            buttonGroup.classList.add('form-open');
        });
    }

    const notifications = document.querySelectorAll('.notification');
    notifications.forEach(notification => {
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 500);
        }, 5000);
    });
});
