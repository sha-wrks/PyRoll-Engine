"""Claude-inspired dark UI theme — colors, fonts, and spacing."""

COLORS = {
    # Backgrounds (dark, warm-tinted)
    "bg_primary":   "#1A1917",
    "bg_secondary": "#221F1D",
    "bg_card":      "#252220",
    "bg_header":    "#0F0D0C",
    "bg_input":     "#2D2A28",
    "bg_hover":     "#302D2B",

    # Accent — Claude coral / terracotta
    "accent_primary": "#D97559",
    "accent_hover":   "#E8896A",

    # Secondary button
    "btn_secondary":       "#3A3530",
    "btn_secondary_hover": "#4A4540",

    # Text
    "text_primary":   "#F0EBE3",
    "text_secondary": "#9B8878",
    "text_muted":     "#6B5E4E",
    "text_on_dark":   "#F0EBE3",
    "text_on_accent": "#FFFFFF",

    # Borders
    "border_light":  "#3A3530",
    "border_medium": "#4A4540",

    # Status
    "success": "#5A9E6F",
    "warning": "#D4A843",
    "error":   "#E05252",
}

FONTS = {
    "heading_lg": ("Segoe UI", 16, "bold"),
    "heading_md": ("Segoe UI", 13, "bold"),
    "body_md":    ("Segoe UI", 11),
    "body_sm":    ("Segoe UI", 10),
    "mono_md":    ("Consolas", 11),
    "label":      ("Segoe UI", 9, "bold"),
}

PAD = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 24,
}
