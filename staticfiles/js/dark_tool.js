document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.className = savedTheme;
    } else {
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.add('light'); 
        }
    }
});

// Toggle dark mode function
function toggleDarkMode() {
    const html = document.documentElement;
    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        html.classList.add('light');
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.remove('light');
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    }
}

// Toggle mobile menu
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    const overlay = document.getElementById('mobile-menu-overlay');
    const body = document.body;
    
    menu.classList.toggle('-translate-x-full');
    overlay.classList.toggle('active');
    body.classList.toggle('mobile-menu-open');
    
    // Close menu when clicking outside
    overlay.onclick = function() {
        menu.classList.add('-translate-x-full');
        overlay.classList.remove('active');
        body.classList.remove('mobile-menu-open');
    };

    // Handle escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && !menu.classList.contains('-translate-x-full')) {
            menu.classList.add('-translate-x-full');
            overlay.classList.remove('active');
            body.classList.remove('mobile-menu-open');
        }
    });
}

function toggleFilterSidebar() {
    const sidebar = document.getElementById('filter-sidebar');
    const overlay = document.getElementById('filter-overlay');
    const body = document.body;

    sidebar.classList.toggle('translate-x-full');
    overlay.classList.toggle('hidden');
    body.classList.toggle('overflow-hidden');
}