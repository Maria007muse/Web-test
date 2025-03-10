document.addEventListener('DOMContentLoaded', () => {
    lottie.loadAnimation({
        container: document.getElementById('laptop-animation'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        path: 'https://lottie.host/38c76355-0b37-4a9a-b27a-670b32466f79/9983VOy5Hr.json'
    });

    const modal = document.getElementById('name-modal');
    document.getElementById('start-test').addEventListener('click', () => modal.style.display = 'flex');

    const nameError = document.getElementById('name-error');
    const nameInput = document.getElementById('user-name');
    const nameForm = document.getElementById('name-form');

    nameForm.addEventListener('submit', (e) => {
        const name = nameInput.value.trim();
        if (!name) {
            e.preventDefault();
            nameError.textContent = 'Пожалуйста, введи своё имя!';
            nameError.style.display = 'block';
            setTimeout(() => nameError.style.display = 'none', 3000);
        } else if (!/^[А-Яа-яA-Za-z\s-]+$/.test(name)) {
            e.preventDefault();
            nameError.textContent = 'Имя должно содержать только буквы, пробелы или дефисы!';
            nameError.style.display = 'block';
            setTimeout(() => nameError.style.display = 'none', 3000);
        }
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
    });
});
