JAZZMIN_SETTINGS = {
    # Site Configuration
    "site_title": "CodeMarket Admin",
    "site_header": "CodeMarket Management System",
    "site_brand": "CodeMarket",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Welcome to CodeMarket Admin Panel",
    "copyright": "CodeMarket © 2024",
    "user_avatar": "profile_picture",
    # Navigation Configuration
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "accounts.customuser"},
        {"model": "projects.project"},
        {"model": "projects.comment"},
        {"model": "projects.projectbase"},
        {"model": "projects.projectimage"},
        {"model": "projects.projectlanguage"},
        {"model": "projects.modelprojectbuy"},
    ],
    # User Menu Configuration
    "usermenu_links": [
        {
            "name": "Documentation",
            "url": "https://docs.codemarket.com",
            "new_window": True,
        },
        {
            "name": "Support",
            "url": "https://support.codemarket.com",
            "new_window": True,
        },
    ],
    # Sidebar Configuration
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_models": [],
    "order_with_respect_to": ["auth", "accounts", "projects"],
    # Icons Configuration
    "icons": {
        # Authentication & Users
        "auth": "fas fa-shield-alt",
        "accounts.customuser": "fas fa-user",
        "auth.Group": "fas fa-users",
        # Projects
        "projects.project": "fas fa-project-diagram",
        "blog.comment": "fas fa-comments",
        "projects.projectbase": "fas fa-database",
        "projects.projectimage": "fas fa-image",
        "blog.post": "fas fa-pencil-alt",
        "projects.modelprojectcomment": "fas fa-check-circle",
        "projects.projectlanguage": "fas fa-code",
        "projects.modelprojectbuy": "fas fa-shopping-cart",
        "blog.tags": "fas fa-tags",
        # Security & Monitoring
        "admin_honeypot.LoginAttempt": "fas fa-user-shield",
        "token_blacklist.BlacklistedToken": "fas fa-ban",
        "token_blacklist.OutstandingToken": "fas fa-history",
        # auth tokens
        "rest_framework.authtoken.Token": "fas fa-key",
        # Analytics
        "hitcount.hitcount": "fas fa-chart-line",
        "hitcount.blacklistip": "fas fa-user-slash",
        "hitcount.blacklistuseragent": "fas fa-user-secret",
        "hitcount.hit": "fas fa-chart-bar",
        "sites.Site": "fas fa-globe",  # Sites
        "socialaccount.SocialAccount": "fas fa-user-circle",  # Social Accounts
        "socialaccount.SocialToken": "fas fa-key",  # Social Application Tokens
        "socialaccount.SocialApp": "fas fa-cogs",  # Social Applications
        "account.EmailAddress": "fas fa-envelope",  # Social Applications
    },
    # Default Icons
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-file",
    # UI Configuration
    "related_modal_active": False,
    "custom_css": "css/admin/custom.css",
    "custom_js": "js/admin/custom.js",
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    # Form Display Configuration
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    # Additional Features
    "language_chooser": True,
    "search_model": "accounts.customuser",
}
