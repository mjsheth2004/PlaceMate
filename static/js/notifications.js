document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var msgs = document.getElementById('global-messages');
        if (msgs) {
            msgs.style.opacity = '0';
            setTimeout(function() {
                msgs.style.display = 'none';
            }, 500);
        }
    }, 2000);
});
