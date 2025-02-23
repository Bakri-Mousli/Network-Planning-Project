# إعدادات الستايل والألوان العامة

# الألوان المطلوبة
PRIMARY_COLOR   = "##d8862c"  # rgb(216, 134, 44)
SECONDARY_COLOR = "#5387D5"  # rgb(83, 135, 213)

# ألوان الخلفيات والإطارات
BACKGROUND_MAIN   = "#F7F7F7"  # لون فاتح للخلفية العامة
BACKGROUND_PANEL  = "#FFF8F0"  # لون خلفية الألواح الجانبية

# إعدادات الخطوط
FONT_MAIN   = ("Helvetica", 12)
FONT_TITLE  = ("Helvetica", 14, "bold")

# إعدادات أزرار ttk
STYLE_BUTTON_OPTIONS = {
    "font": FONT_MAIN,
    "padding": 6,
    "background": SECONDARY_COLOR,
    "foreground": "white"
}

# إعدادات تسميات ttk
STYLE_LABEL_OPTIONS = {
    "font": FONT_MAIN,
    "padding": 4,
    "background": BACKGROUND_PANEL,
    "foreground": "black"
}
