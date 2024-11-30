from .ckeditor_storage import CustomStorage

customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

CKEDITOR_5_CUSTOM_CSS = "css/style.css"
CKEDITOR_5_FILE_STORAGE = "config.ckeditor_storage.CustomStorage"
CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "imageUpload",
            "|",
            "undo",
            "redo",
            "|",
            "codeBlock",
        ],
        "language": "en",
    },
    "extends": {
        "blockToolbar": [
            "paragraph",
            "heading1",
            "heading2",
            "heading3",
            "|",
            "bulletedList",
            "numberedList",
            "|",
            "blockQuote",
        ],
        "toolbar": [
            "heading",
            "|",
            "outdent",
            "indent",
            "|",
            "bold",
            "italic",
            "link",
            "underline",
            "strikethrough",
            "code",
            "subscript",
            "superscript",
            "highlight",
            "|",
            "codeBlock",
            "sourceEditing",
            "insertImage",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "blockQuote",
            "imageUpload",
            "|",
            "fontSize",
            "fontFamily",
            "fontColor",
            "fontBackgroundColor",
            "mediaEmbed",
            "removeFormat",
            "insertTable",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h3",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
        "codeBlock": {
            "languages": [
                {"language": "plaintext", "label": "Plain text", "class": ""},
                {"language": "python", "label": "Python", "class": "language-python"},
                {
                    "language": "javascript",
                    "label": "JavaScript",
                    "class": "language-javascript",
                },
                {"language": "html", "label": "HTML", "class": "language-html"},
                {"language": "css", "label": "CSS", "class": "language-css"},
                {"language": "bash", "label": "Bash", "class": "language-bash"},
                {"language": "json", "label": "JSON", "class": "language-json"},
                {"language": "yaml", "label": "YAML", "class": "language-yaml"},
                {"language": "sql", "label": "SQL", "class": "language-sql"},
                {"language": "php", "label": "PHP", "class": "language-php"},
                {"language": "ruby", "label": "Ruby", "class": "language-ruby"},
                {"language": "go", "label": "Go", "class": "language-go"},
                {"language": "rust", "label": "Rust", "class": "language-rust"},
                {"language": "kotlin", "label": "Kotlin", "class": "language-kotlin"},
                {"language": "swift", "label": "Swift", "class": "language-swift"},
                {
                    "language": "typescript",
                    "label": "TypeScript",
                    "class": "language-typescript",
                },
                {"language": "java", "label": "Java", "class": "language-java"},
                {"language": "c++", "label": "C++", "class": "language-cpp"},
                {"language": "c#", "label": "C#", "class": "language-csharp"},
                {"language": "kotlin", "label": "Kotlin", "class": "language-kotlin"},
            ]
        },
    },
    "list": {
        "properties": {
            "styles": True,
            "startIndex": True,
            "reversed": True,
        }
    },
}

CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
CKEDITOR_5_UPLOAD_FILE_VIEW_NAME = "custom_upload_file"
