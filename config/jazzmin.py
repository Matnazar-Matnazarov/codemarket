JAZZMIN_SETTINGS = {
    "site_title": "Django Admin",
    "site_header": "Management System",
    "site_brand": "Django Admin",
    # "login_logo": "img/login_logo.png",
    # "login_logo_dark": "img/login_logo_dark.png",
    "site_logo_classes": "img-circle",
    # "site_icon": "img/favicon.ico",
    "welcome_sign": "Welcome to the Library Admin Panel",
    "copyright": "Acme Library Ltd",
    "user_avatar": "profile_picture",
    # Top Menu
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "accounts.customuser"},
        {"model": "app1.Genre"},
        {"model": "app1.Author"},
        {"model": "app1.Music_file"},
        {"model": "app1.Music"},
        {"model": "app1.UserComment"},
        {"model": "app1.TelegramUser"},
    ],
    # User Menu
    "usermenu_links": [
        {"name": "Support", "url": "https://support.example.com", "new_window": True},
    ],
    # Side Menu
    "show_sidebar": True,
    "navigation_expanded": True,
    # "hide_apps": ['hitcount'],
    "hide_models": [],
    "order_with_respect_to": ["auth", "app1", "accounts", "customuser"],
    # Icons
    "icons": {
        "auth": "fas fa-users-cog",
        # "auth.user": "fas fa-user",
        "accounts.customuser": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app1.Genre": "fas fa-tag",
        "app1.Author": "fas fa-user-edit",
        "app1.Music_file": "fas fa-file-audio",
        "app1.Music": "fas fa-music",
        "app1.user_comment": "fas fa-comments",
        "app1.telegram_user": "fas fa-people-carry",
        "hitcount.hitcount": "fas fa-chart-line",
        "hitcount.blacklistip": "fas fa-ban",  # Icon for Blacklisted IPs
        "hitcount.blacklistuseragent": "fas fa-user-secret",  # Icon for Blacklisted User Agents
        "hitcount.hit": "fas fa-crown",
        "easyaudit.LoginEvent": "fas fa-file-alt",  # Requests audit uchun
        "easyaudit.ModelChangeEvent": "fas fa-history",  # Model changes audit
        "easyaudit.CRUDEvent": "fas fa-tasks",  # CRUD event audit
        # CRUD uchun alohida iconlar
        "easyaudit.CRUDEvent.CREATE": "fas fa-plus-circle",  # Create uchun
        "easyaudit.CRUDEvent.UPDATE": "fas fa-edit",  # Update uchun
        "easyaudit.CRUDEvent.DELETE": "fas fa-trash",  # Delete uchun
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    # Related Modal
    "related_modal_active": False,
    # UI Tweaks
    "custom_css": "css/custom_admin.css",
    "custom_js": "js/custom_admin.js",
    "use_google_fonts_cdn": True,
    "show_ui_builder": True,
    # Change view
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": True,
}
