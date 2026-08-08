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
});
