document.addEventListener('DOMContentLoaded', function () {
    // Auto submit form when status dropdown changes
    const autoSubmitSelects = document.querySelectorAll('.auto-submit-status');
    autoSubmitSelects.forEach(function (select) {
        select.addEventListener('change', function () {
            if (this.form) {
                this.form.submit();
            }
        });
    });

    // File input label display update for company logo
    const logoInput = document.getElementById('id_logo');
    const logoName = document.getElementById('logo-file-name');
    if (logoInput && logoName) {
        logoInput.addEventListener('change', function () {
            if (this.files && this.files.length > 0) {
                logoName.textContent = this.files[0].name;
            } else {
                logoName.textContent = 'No file chosen';
            }
        });
    }
});
