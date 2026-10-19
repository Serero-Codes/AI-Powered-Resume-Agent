"""Centralized design settings for generated CV documents."""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

# --------------------------------------------------

# PAGE SETTINGS

# --------------------------------------------------

PAGE_SIZE = A4

PAGE_MARGIN_LEFT = 1.6 * 28.3465
PAGE_MARGIN_RIGHT = 1.6 * 28.3465
PAGE_MARGIN_TOP = 1.4 * 28.3465
PAGE_MARGIN_BOTTOM = 1.4 * 28.3465

MAX_PAGES = 2

# --------------------------------------------------

# FONT SETTINGS

# --------------------------------------------------

FONT_REGULAR = "Helvetica"
FONT_BOLD = "Helvetica-Bold"

NAME_FONT_SIZE = 24
SECTION_HEADING_SIZE = 12
JOB_TITLE_SIZE = 10.5
BODY_FONT_SIZE = 9.5
CONTACT_FONT_SIZE = 9

MIN_BODY_FONT_SIZE = 9
MAX_BODY_FONT_SIZE = 10.5

# --------------------------------------------------

# COLOUR SETTINGS

# --------------------------------------------------

TEXT_COLOR = colors.HexColor("#242424")
HEADING_COLOR = colors.HexColor("#172554")
ACCENT_COLOR = colors.HexColor("#2563EB")
MUTED_COLOR = colors.HexColor("#525252")
DIVIDER_COLOR = colors.HexColor("#CBD5E1")
BACKGROUND_COLOR = colors.white

# --------------------------------------------------

# SPACING SETTINGS

# --------------------------------------------------

NAME_BOTTOM_SPACE = 4
CONTACT_BOTTOM_SPACE = 10
SECTION_TOP_SPACE = 8
SECTION_BOTTOM_SPACE = 4
PARAGRAPH_SPACE = 3
BULLET_SPACE = 2
EXPERIENCE_ENTRY_SPACE = 5
PROJECT_ENTRY_SPACE = 5

# --------------------------------------------------

# CV SECTION ORDER

# --------------------------------------------------

SECTION_ORDER = [
"professional_summary",
"technical_skills",
"soft_skills",
"experience",
"projects",
"certifications",
"education",
]

# --------------------------------------------------

# CONTENT LIMITS

# --------------------------------------------------

MAX_SUMMARY_WORDS = 90
MAX_BULLETS_PER_EXPERIENCE = 5
MAX_BULLETS_PER_PROJECT = 4
MAX_TECHNICAL_SKILLS_PER_CATEGORY = 10
