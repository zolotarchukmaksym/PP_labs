document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.btn-danger[data-confirm]');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            const message = button.getAttribute('data-confirm');
            const isConfirmed = confirm(message);

            if (!isConfirmed) {
                event.preventDefault();
            }
        });
    });
});
