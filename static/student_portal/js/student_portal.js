document.addEventListener('DOMContentLoaded', function () {
    // Photo Modal Lightbox toggle for Profile Page
    const photoModal = document.getElementById('photoModal');
    const photoTrigger = document.getElementById('photoModalTrigger');
    const photoCloseBtn = document.getElementById('photoModalClose');

    if (photoTrigger && photoModal) {
        photoTrigger.addEventListener('click', function () {
            photoModal.classList.add('active');
        });
    }

    if (photoModal) {
        photoModal.addEventListener('click', function (e) {
            if (e.target === photoModal || e.target === photoCloseBtn) {
                photoModal.classList.remove('active');
            }
        });
    }

    // Confirmation for Apply Form
    const applyForms = document.querySelectorAll('form.apply-drive-form');
    applyForms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const confirmed = confirm('Are you sure you want to apply for this drive? This action cannot be undone.');
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });
});
