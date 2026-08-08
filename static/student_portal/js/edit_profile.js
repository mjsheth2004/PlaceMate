document.addEventListener('DOMContentLoaded', function() {
    const resumeInput = document.getElementById('id_resume');
    const photoInput = document.getElementById('id_profile_photo');
    const resumeName = document.getElementById('resume-file-name');
    const photoName = document.getElementById('photo-file-name');

    if (resumeInput) {
        resumeInput.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                resumeName.textContent = this.files[0].name;
            } else {
                resumeName.textContent = 'No file chosen';
            }
        });
    }

    if (photoInput) {
        photoInput.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                photoName.textContent = this.files[0].name;
            } else {
                photoName.textContent = 'No file chosen';
            }
        });
    }
});
