document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    function toggleSidebar() {
        if (sidebar) sidebar.classList.toggle('open');
        if (sidebarOverlay) sidebarOverlay.classList.toggle('active');
    }

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', toggleSidebar);
    }

    const themeCheckboxes = document.querySelectorAll('input[type="checkbox"][id^="themeToggle"]');
    
    function applyTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.body.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            themeCheckboxes.forEach(cb => cb.checked = true);
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            document.body.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
            themeCheckboxes.forEach(cb => cb.checked = false);
        }
        
        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: theme } }));
    }

    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme ? savedTheme : (prefersDark ? 'dark' : 'light');
    
    applyTheme(initialTheme);

    themeCheckboxes.forEach(themeCheckbox => {
        themeCheckbox.addEventListener('change', function() {
            const isDark = this.checked;
            applyTheme(isDark ? 'dark' : 'light');
        });
    });
});
