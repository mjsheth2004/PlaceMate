/**
 * PlaceMate Global Theme Switcher
 * Handles synchronization between localStorage, HTML data-theme, and theme toggle buttons.
 * Defaults to Light Mode unless explicitly set to 'dark' by the user.
 */
(function () {
    function applyTheme(theme) {
        var isDark = (theme === 'dark');
        var themeValue = isDark ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', themeValue);
        if (document.body) {
            document.body.setAttribute('data-theme', themeValue);
        }
        localStorage.setItem('theme', themeValue);

        // Update all theme toggle checkboxes on the page
        var checkboxes = document.querySelectorAll('input[type="checkbox"][id*="themeToggle"], input[type="checkbox"][id*="ThemeToggle"]');
        checkboxes.forEach(function (cb) {
            cb.checked = isDark;
        });

        window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: themeValue } }));
    }

    function initThemeToggles() {
        var savedTheme = localStorage.getItem('theme');
        // Defaults to light mode
        var currentTheme = (savedTheme === 'dark') ? 'dark' : 'light';
        applyTheme(currentTheme);

        var checkboxes = document.querySelectorAll('input[type="checkbox"][id*="themeToggle"], input[type="checkbox"][id*="ThemeToggle"]');
        checkboxes.forEach(function (cb) {
            cb.checked = (currentTheme === 'dark');
            cb.removeEventListener('change', handleToggleChange);
            cb.addEventListener('change', handleToggleChange);
        });
    }

    function handleToggleChange() {
        applyTheme(this.checked ? 'dark' : 'light');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initThemeToggles);
    } else {
        initThemeToggles();
    }
})();
