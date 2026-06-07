from django.db import models
from wagtail.models import Page, Orderable
from wagtail.admin.panels import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
)
from wagtail.documents.models import AbstractDocument
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from cloudinary_storage.storage import RawMediaCloudinaryStorage


# ──────────────────────────────────────────────
# CUSTOM DOCUMENT MODEL (stores PDFs/files as Cloudinary raw resources)
# ──────────────────────────────────────────────

class CustomDocument(AbstractDocument):
    file = models.FileField(
        upload_to="documents",
        storage=RawMediaCloudinaryStorage(),
        verbose_name="File",
    )
    admin_form_fields = ("title", "file", "collection", "tags")


# ──────────────────────────────────────────────
# NAVBAR
# ──────────────────────────────────────────────

class NavbarMenu(ClusterableModel, Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="navbar_menus")
    title = models.CharField(max_length=100)
    url = models.CharField(
        max_length=255, blank=True, default="",
        help_text="Direct link URL. Leave blank if this item has dropdown sub-items.",
    )

    panels = [
        FieldRowPanel([FieldPanel("title"), FieldPanel("url")]),
        InlinePanel("menu_items", label="Dropdown Items (leave empty if using a direct URL above)"),
    ]

    def __str__(self):
        return self.title


class NavbarMenuItem(Orderable):
    menu = ParentalKey("NavbarMenu", on_delete=models.CASCADE, related_name="menu_items")
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255)

    panels = [
        FieldPanel("label"),
        FieldPanel("url"),
    ]

    def __str__(self):
        return self.label


HOME_ICON_CHOICES = [
    ("fa-solid fa-graduation-cap", "Graduation Cap"),
    ("fa-solid fa-book-open",       "Book Open"),
    ("fa-solid fa-trophy",          "Trophy"),
    ("fa-solid fa-medal",           "Medal"),
    ("fa-solid fa-star",            "Star"),
    ("fa-solid fa-users",           "Group / Students"),
    ("fa-solid fa-chalkboard-user", "Teacher"),
    ("fa-solid fa-school",          "School Building"),
    ("fa-solid fa-microscope",      "Science Lab"),
    ("fa-solid fa-computer",        "Computer / IT"),
    ("fa-solid fa-moon",            "Islamic Studies"),
    ("fa-solid fa-flag",            "Pakistan Studies"),
    ("fa-solid fa-shield-halved",   "Excellence / Discipline"),
    ("fa-solid fa-heart",           "Values / Character"),
    ("fa-solid fa-lightbulb",       "Innovation / Ideas"),
    ("fa-solid fa-award",           "Award / Recognition"),
    ("fa-solid fa-check-double",    "Quality Assurance"),
    ("fa-solid fa-person-running",  "Sports / PE"),
    ("fa-solid fa-palette",         "Arts & Craft"),
    ("fa-solid fa-calculator",      "Mathematics"),
    ("fa-solid fa-flask",           "Chemistry"),
    ("fa-solid fa-atom",            "Physics"),
    ("fa-solid fa-dna",             "Biology"),
    ("fa-solid fa-language",        "Languages"),
    ("fa-solid fa-pen-nib",         "Urdu / Writing"),
    ("fa-solid fa-earth-asia",      "General Knowledge"),
    ("fa-solid fa-bullhorn",        "Announcement"),
    ("fa-solid fa-calendar-check",  "Events / Schedule"),
    ("fa-solid fa-door-open",       "Admissions"),
    ("fa-solid fa-file-pen",        "Exams / Tests"),
]

# ──────────────────────────────────────────────
# TRUST SECTION
# ──────────────────────────────────────────────

class TrustCard(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="trust_cards")
    icon_class = models.CharField(
        max_length=100, choices=HOME_ICON_CHOICES,
        default="fa-solid fa-graduation-cap",
        help_text="Choose a Font Awesome icon — no image upload needed.",
    )
    logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="trust_card_logo",
        help_text="Optional: upload an image to override the icon above.",
    )
    heading = models.CharField(max_length=200)
    description = models.TextField()

    panels = [
        FieldPanel("icon_class"),
        FieldPanel("logo"),
        FieldPanel("heading"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.heading


# ──────────────────────────────────────────────
# BOARDS SECTION
# ──────────────────────────────────────────────

BOARD_TAB_CHOICES = [
    ("all",          "All"),
    ("matric",       "Matric"),
    ("intermediate", "Intermediate"),
    ("cambridge",    "Cambridge"),
    ("primary",      "Primary"),
]


class BoardCard(Orderable):
    """
    One card in the Boards section on the homepage.
    Each card shows as a premium 2-column card with a dark gradient header.
    Cards alternate colour: odd = navy (BSEK style), even = green (Aga Khan style).

    Example setup for Azeem School:
    ─────────────────────────────────────────────────────────────────────
    Card 1 — BSEK Matric
      Tab:         Matric
      Icon:        Book Open Reader
      Board Name:  BSEK  (Matric — Class 9 & 10)
      Level Label: Class 9 – 10
      Description: Nationally recognised qualification aligned with Pakistan's federal curriculum...
      Subjects:    Physics, Chemistry, Biology, Mathematics, Urdu, Pakistan Studies, Islamiyat
      Link:        /academics/

    Card 2 — Aga Khan O/A Level
      Tab:         Cambridge
      Icon:        Globe
      Board Name:  Aga Khan Board  (AKUEB — O & A Level)
      Level Label: O Level & A Level
      Description: Internationally recognised qualifications, accepted by top universities worldwide...
      Subjects:    Physics, Chemistry, Biology, Mathematics, English, Business Studies, ICT
      Link:        /academics/
    ─────────────────────────────────────────────────────────────────────
    """

    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="board_cards")

    tab = models.CharField(
        max_length=20, choices=BOARD_TAB_CHOICES, default="all",
        verbose_name="Category Tab",
        help_text="Which board category this card belongs to. e.g. Matric, Intermediate, Cambridge, Primary.",
    )
    icon_class = models.CharField(
        max_length=100, choices=HOME_ICON_CHOICES,
        default="fa-solid fa-graduation-cap",
        verbose_name="Card Icon",
        help_text="Icon shown in the coloured header. Choose from the dropdown — no image upload needed.",
    )
    board_name = models.CharField(
        max_length=200,
        verbose_name="Board / Programme Name",
        help_text='Full name shown as the card title.  e.g.  BSEK  (Matric — Class 9 & 10)',
    )
    level_label = models.CharField(
        max_length=100, blank=True,
        verbose_name="Level / Class Range",
        help_text='Shown as a small label below the board name.  e.g.  Class 9 – 10   or   O Level & A Level',
    )
    description = models.TextField(
        verbose_name="Description",
        help_text=(
            "2–3 sentences about this board/programme.  "
            "e.g.  Nationally recognised Matric qualification aligned with Pakistan's federal curriculum, "
            "preparing students for competitive examinations across the country."
        ),
    )
    subjects_list = models.CharField(
        max_length=400, blank=True,
        verbose_name="Subjects (comma-separated)",
        help_text=(
            "Type subjects separated by commas — they appear as tags on the card.  "
            "e.g.  Physics, Chemistry, Biology, Mathematics, Urdu, Islamiyat"
        ),
    )
    learn_more_url = models.CharField(
        max_length=255, blank=True,
        verbose_name="'Explore Program' Button URL",
        help_text='URL the Explore Program button links to.  e.g.  /academics/',
    )

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel("tab"),
                FieldPanel("icon_class"),
            ]),
        ], heading="Category & Icon"),
        MultiFieldPanel([
            FieldPanel("board_name"),
            FieldPanel("level_label"),
            FieldPanel("description"),
        ], heading="Card Content"),
        MultiFieldPanel([
            FieldPanel("subjects_list"),
            FieldPanel("learn_more_url"),
        ], heading="Subjects & Link"),
    ]

    @property
    def subjects_as_list(self):
        return [s.strip() for s in self.subjects_list.split(",") if s.strip()]

    def __str__(self):
        return self.board_name


# ──────────────────────────────────────────────
# FACILITIES TEASER SECTION
# ──────────────────────────────────────────────

FAC_ICON_COLOR_CHOICES = [
    ("",        "Gold (default)"),
    ("#1565c0", "Blue"),
    ("#16a34a", "Green"),
    ("#ca8a04", "Amber / Yellow"),
    ("#ec407a", "Pink / Red"),
    ("#ab47bc", "Purple"),
    ("#0097a7", "Teal / Cyan"),
    ("#e65100", "Orange"),
    ("#1f1741", "Dark Navy"),
]


class HomeFacilityCard(Orderable):
    """
    One card in the Facilities Teaser section (4 cards recommended).

    Example setup:
      Card 1 — Computer Labs
        Image:       Upload a photo of the computer lab
        Icon:        Computer / IT
        Icon Colour: Blue
        Title:       Computer Labs
        Description: Modern PCs, high-speed internet and coding tools for all grades.
        Link:        /facilities/

      Card 2 — Science Labs
        Icon: Microscope   Colour: Green

      Card 3 — Digital Library
        Icon: Book Open    Colour: Amber / Yellow

      Card 4 — Sports Grounds
        Icon: Sports / PE  Colour: Pink / Red
    """

    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="facility_teasers")

    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="facility_teaser_image",
        verbose_name="Background Image",
        help_text="Photo shown as the card background.",
    )
    icon_class = models.CharField(
        max_length=100, choices=HOME_ICON_CHOICES,
        default="fa-solid fa-school",
        verbose_name="Card Icon",
    )
    icon_bg_color = models.CharField(
        max_length=30, blank=True, default="",
        choices=FAC_ICON_COLOR_CHOICES,
        verbose_name="Icon Background Colour",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Facility Name",
        help_text='e.g.  Computer Labs',
    )
    description = models.CharField(
        max_length=300,
        verbose_name="Short Description",
        help_text='One sentence.  e.g.  Modern PCs, high-speed internet and coding tools for all grades.',
    )
    link_url = models.CharField(
        max_length=255, blank=True, default="/facilities/",
        verbose_name="Card Link URL",
        help_text="Default:  /facilities/",
    )

    panels = [
        FieldPanel("image"),
        FieldRowPanel([FieldPanel("icon_class"), FieldPanel("icon_bg_color")]),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("link_url"),
    ]

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
# ABOUT SECTION
# ──────────────────────────────────────────────

class AboutFeature(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="about_features")
    text = models.CharField(max_length=300)

    panels = [FieldPanel("text")]

    def __str__(self):
        return self.text


# ──────────────────────────────────────────────
# COURSES SECTION
# ──────────────────────────────────────────────

class CourseCard(Orderable):
    TAB_CHOICES = [
        ("all", "All"),
        ("design", "Design"),
        ("data-science", "Data Science"),
        ("marketing", "Marketing"),
        ("development", "Development"),
    ]

    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="course_cards")
    image = models.ForeignKey(
        "wagtailimages.Image", null=True,
        on_delete=models.SET_NULL, related_name="course_card_image",
    )

    tab = models.CharField(max_length=20, choices=TAB_CHOICES, default="all")
    title = models.CharField(max_length=200)
    lessons_count = models.CharField(max_length=20, default="", help_text='e.g. "8 Lessons"')
    students_count = models.CharField(max_length=20, default="", help_text='e.g. "70 Students"')
    price = models.CharField(max_length=20, default="", help_text='e.g. "$87"')
    modal_description = models.TextField(default="")
    modal_btn_label = models.CharField(max_length=50, default="Read More")
    modal_btn_url = models.CharField(max_length=255, default="")

    panels = [
        FieldPanel("image"),
        FieldRowPanel([FieldPanel("tab"), FieldPanel("price")]),
        FieldPanel("title"),
        FieldRowPanel([FieldPanel("lessons_count"), FieldPanel("students_count")]),
        FieldPanel("modal_description"),
        FieldRowPanel([FieldPanel("modal_btn_label"), FieldPanel("modal_btn_url")]),
    ]

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
# BENEFITS / COUNTER STATS
# ──────────────────────────────────────────────

class BenefitCard(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="benefit_cards")
    counter = models.CharField(max_length=20, help_text='e.g. "95"')
    suffix = models.CharField(max_length=5, blank=True, help_text='e.g. "%", "+"')
    label = models.CharField(max_length=100)

    panels = [
        FieldRowPanel([FieldPanel("counter"), FieldPanel("suffix")]),
        FieldPanel("label"),
    ]

    def __str__(self):
        return f"{self.counter}{self.suffix} — {self.label}"


# ──────────────────────────────────────────────
# TESTIMONIALS
# ──────────────────────────────────────────────

class Testimonial(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="testimonials")
    photo = models.ForeignKey(
        "wagtailimages.Image", null=True,
        on_delete=models.SET_NULL, related_name="testimonial_photo",
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default="Happy Client")
    quote = models.TextField()

    panels = [
        FieldPanel("photo"),
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("quote"),
    ]

    def __str__(self):
        return self.name


# ──────────────────────────────────────────────
# BLOG / ARTICLES
# ──────────────────────────────────────────────

class BlogPost(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="blog_posts")
    image = models.ForeignKey(
        "wagtailimages.Image", null=True,
        on_delete=models.SET_NULL, related_name="blog_post_image",
    )
    date = models.DateField()
    title = models.CharField(max_length=300)
    excerpt = models.TextField()
    url = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("date"),
        FieldPanel("title"),
        FieldPanel("excerpt"),
        FieldPanel("url"),
    ]

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
# NOTICES / ANNOUNCEMENTS
# ──────────────────────────────────────────────

class HomeNotice(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="home_notices")
    icon_class = models.CharField(
        max_length=100, choices=HOME_ICON_CHOICES,
        default="fa-solid fa-bullhorn",
    )
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    url = models.CharField(max_length=255, blank=True)
    is_urgent = models.BooleanField(default=False,
                                    help_text="Highlights notice in accent colour — use for time-sensitive items.")

    panels = [
        FieldRowPanel([FieldPanel("icon_class"), FieldPanel("is_urgent")]),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldRowPanel([FieldPanel("date"), FieldPanel("url")]),
    ]

    def __str__(self):
        return self.title


# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────

class FooterSocialLink(Orderable):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("youtube", "YouTube"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
    ]

    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="footer_social_links")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()

    panels = [FieldPanel("platform"), FieldPanel("url")]

    def __str__(self):
        return self.platform


class FooterUsefulLink(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="footer_useful_links")
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255)

    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label


class FooterExploreLink(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="footer_explore_links")
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255)

    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label


# ──────────────────────────────────────────────
# ADMISSIONS PAGE — INLINE MODELS
# ──────────────────────────────────────────────

class AdmissionStat(Orderable):
    page = ParentalKey("AdmissionsPage", on_delete=models.CASCADE, related_name="admission_stats")
    number = models.CharField(max_length=20, help_text='e.g. "98", "5K", "120"')
    suffix = models.CharField(max_length=10, blank=True, help_text='e.g. "%", "+", "K+", "h"')
    label = models.CharField(max_length=150)

    panels = [
        FieldRowPanel([FieldPanel("number"), FieldPanel("suffix")]),
        FieldPanel("label"),
    ]

    def __str__(self):
        return f"{self.number}{self.suffix} — {self.label}"


class AdmissionRequirement(Orderable):
    page = ParentalKey("AdmissionsPage", on_delete=models.CASCADE, related_name="admission_requirements")
    icon_class = models.CharField(max_length=100, default="fa-solid fa-check",
                                  help_text='Font Awesome class, e.g. "fa-solid fa-graduation-cap"')
    title = models.CharField(max_length=200)
    description = models.TextField()

    panels = [FieldPanel("icon_class"), FieldPanel("title"), FieldPanel("description")]

    def __str__(self):
        return self.title


class AdmissionIntakeCard(Orderable):
    BG_CHOICES = [
        ("bg1", "Green (bg1)"),
        ("bg2", "Yellow (bg2)"),
        ("bg3", "Red (bg3)"),
    ]
    page = ParentalKey("AdmissionsPage", on_delete=models.CASCADE, related_name="admission_intake_cards")
    bg_choice = models.CharField(max_length=10, choices=BG_CHOICES, default="bg1")
    icon_class = models.CharField(max_length=100, default="fa-solid fa-calendar-check",
                                  help_text='Font Awesome class, e.g. "fa-solid fa-calendar-check"')
    title = models.CharField(max_length=200)
    description = models.TextField()

    panels = [
        FieldRowPanel([FieldPanel("bg_choice"), FieldPanel("icon_class")]),
        FieldPanel("title"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.title


class AdmissionStep(Orderable):
    page = ParentalKey("AdmissionsPage", on_delete=models.CASCADE, related_name="admission_steps")
    step_number = models.CharField(max_length=5, help_text='e.g. "01", "02"')
    title = models.CharField(max_length=200)
    description = models.TextField()

    panels = [FieldPanel("step_number"), FieldPanel("title"), FieldPanel("description")]

    def __str__(self):
        return f"{self.step_number} — {self.title}"


class AdmissionFormInfo(Orderable):
    page = ParentalKey("AdmissionsPage", on_delete=models.CASCADE, related_name="admission_form_infos")
    icon_class = models.CharField(max_length=100, default="fa-solid fa-bolt",
                                  help_text='Font Awesome class, e.g. "fa-solid fa-bolt"')
    title = models.CharField(max_length=200)
    description = models.TextField()

    panels = [FieldPanel("icon_class"), FieldPanel("title"), FieldPanel("description")]

    def __str__(self):
        return self.title


class AdmissionCampus(Orderable):
    page = ParentalKey("AdmissionsPage", on_delete=models.CASCADE, related_name="admission_campuses")
    name = models.CharField(max_length=200, help_text='e.g. "Azeem - KDA Campus"')

    panels = [FieldPanel("name")]

    def __str__(self):
        return self.name


class AdmissionBoard(Orderable):
    page = ParentalKey("AdmissionsPage", on_delete=models.CASCADE, related_name="admission_boards")
    name = models.CharField(max_length=200, help_text='e.g. "Sindh Board"')

    panels = [FieldPanel("name")]

    def __str__(self):
        return self.name


# ── Admissions footer inline models ───────────

class AdmissionsFooterSocialLink(Orderable):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("youtube", "YouTube"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
    ]
    page = ParentalKey("AdmissionsPage", on_delete=models.CASCADE, related_name="admissions_footer_social_links")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    panels = [FieldPanel("platform"), FieldPanel("url")]

    def __str__(self):
        return self.platform


class AdmissionsFooterUsefulLink(Orderable):
    page = ParentalKey("AdmissionsPage", on_delete=models.CASCADE, related_name="admissions_footer_useful_links")
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label


class AdmissionsFooterExploreLink(Orderable):
    page = ParentalKey("AdmissionsPage", on_delete=models.CASCADE, related_name="admissions_footer_explore_links")
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label


# ──────────────────────────────────────────────
# ADMISSIONS PAGE
# ──────────────────────────────────────────────

class AdmissionsPage(Page):

    # ── Navbar ────────────────────────────────
    nav_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="admissions_nav_logo",
        verbose_name="Navbar Logo",
    )
    nav_phone = models.CharField(max_length=30, default="")
    nav_login_label = models.CharField(max_length=50, default="Log In")
    nav_login_url = models.CharField(max_length=255, default="#")

    # ── Sub-Banner ────────────────────────────
    banner_bg_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="admissions_banner_bg",
        verbose_name="Banner Background Image",
        help_text="Recommended resolution: 1920 × 486 px",
    )
    banner_title = models.CharField(max_length=200, default="Start Your Journey With Us")
    banner_description = models.TextField(default="")

    # ── Requirements Section ──────────────────
    requirements_subtitle = models.CharField(max_length=100, default="Who Can Apply")
    requirements_heading = models.CharField(max_length=300, default="Eligibility & Requirements")

    # ── Process Section ───────────────────────
    process_subtitle = models.CharField(max_length=100, default="Simple & Fast")
    process_heading = models.CharField(max_length=300, default="How Our Admissions Works")

    # ── Form Section ──────────────────────────
    form_subtitle = models.CharField(max_length=100, default="Apply Now")
    form_heading = models.CharField(max_length=300, default="Your Future Starts With One Form")
    form_intro_text = models.TextField(default="")
    form_contact_email = models.EmailField(default="admissions@educiza.com")
    form_submit_label = models.CharField(max_length=100, default="Submit My Application")
    form_success_message = models.TextField(
        default="Application submitted! Our admissions team will contact you within 48 hours.")

    # ── Footer ────────────────────────────────
    footer_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="admissions_footer_logo",
    )
    footer_newsletter_heading = models.CharField(max_length=200, default="Sign up for the newsletter:")
    footer_about_title = models.CharField(max_length=100, default="About Us")
    footer_about_text = models.TextField(default="")
    footer_links_title = models.CharField(max_length=100, default="Useful Links")
    footer_explore_title = models.CharField(max_length=100, default="Programs")
    footer_contact_title = models.CharField(max_length=100, default="Contact Us")
    footer_contact_phone = models.CharField(max_length=30, default="")
    footer_contact_email = models.EmailField(default="")
    footer_contact_address = models.CharField(max_length=300, default="")
    footer_contact_map_url = models.URLField(blank=True)
    footer_copyright_text = models.CharField(max_length=200, default="")

    # ──────────────────────────────────────────
    # ADMIN PANELS
    # ──────────────────────────────────────────

    content_panels = Page.content_panels + [

        MultiFieldPanel([
            FieldPanel("nav_logo"),
            FieldPanel("nav_phone"),
            FieldRowPanel([FieldPanel("nav_login_label"), FieldPanel("nav_login_url")]),
        ], heading="Navbar"),

        MultiFieldPanel([
            FieldPanel("banner_bg_image"),
            FieldPanel("banner_title"),
            FieldPanel("banner_description"),
        ], heading="Sub-Banner"),

        MultiFieldPanel([
            InlinePanel("admission_stats", label="Stats"),
        ], heading="Stats Strip"),

        MultiFieldPanel([
            FieldPanel("requirements_subtitle"),
            FieldPanel("requirements_heading"),
            InlinePanel("admission_requirements", label="Requirements"),
            InlinePanel("admission_intake_cards", label="Intake / Info Cards"),
        ], heading="Requirements Section"),

        MultiFieldPanel([
            FieldPanel("process_subtitle"),
            FieldPanel("process_heading"),
            InlinePanel("admission_steps", label="Steps"),
        ], heading="Admissions Process Steps"),

        MultiFieldPanel([
            FieldPanel("form_subtitle"),
            FieldPanel("form_heading"),
            FieldPanel("form_intro_text"),
            FieldPanel("form_contact_email"),
            FieldPanel("form_submit_label"),
            FieldPanel("form_success_message"),
            InlinePanel("admission_form_infos", label="Left Panel Info Items"),
            InlinePanel("admission_campuses", label="Campus Dropdown Options"),
            InlinePanel("admission_boards", label="Board Selection Options"),
        ], heading="Application Form Section"),

        MultiFieldPanel([
            FieldPanel("footer_logo"),
            FieldPanel("footer_newsletter_heading"),
            FieldPanel("footer_about_title"),
            FieldPanel("footer_about_text"),
            InlinePanel("admissions_footer_social_links", label="Social Links"),
            FieldPanel("footer_links_title"),
            InlinePanel("admissions_footer_useful_links", label="Useful Links"),
            FieldPanel("footer_explore_title"),
            InlinePanel("admissions_footer_explore_links", label="Explore / Programs Links"),
            FieldPanel("footer_contact_title"),
            FieldRowPanel([FieldPanel("footer_contact_phone"), FieldPanel("footer_contact_email")]),
            FieldPanel("footer_contact_address"),
            FieldPanel("footer_contact_map_url"),
            FieldPanel("footer_copyright_text"),
        ], heading="Footer"),
    ]

    class Meta:
        verbose_name = "Admissions Page"


# ──────────────────────────────────────────────
# ABOUT PAGE — INLINE MODELS
# ──────────────────────────────────────────────

class AboutPageFeature(Orderable):
    page = ParentalKey("AboutPage", on_delete=models.CASCADE, related_name="about_features")
    text = models.CharField(max_length=300)

    panels = [FieldPanel("text")]

    def __str__(self):
        return self.text


class AboutChooseFeature(Orderable):
    page = ParentalKey("AboutPage", on_delete=models.CASCADE, related_name="choose_features")
    icon = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="about_choose_icon",
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    link_url = models.CharField(max_length=255, blank=True, default="./about.html")

    panels = [
        FieldPanel("icon"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("link_url"),
    ]

    def __str__(self):
        return self.title


class AboutBenefitStat(Orderable):
    page = ParentalKey("AboutPage", on_delete=models.CASCADE, related_name="benefit_stats")
    counter = models.CharField(max_length=20, help_text='e.g. "95"')
    suffix = models.CharField(max_length=5, blank=True, help_text='e.g. "%", "+"')
    label = models.CharField(max_length=100)

    panels = [
        FieldRowPanel([FieldPanel("counter"), FieldPanel("suffix")]),
        FieldPanel("label"),
    ]

    def __str__(self):
        return f"{self.counter}{self.suffix} — {self.label}"


class AboutTeamMember(Orderable):
    page = ParentalKey("AboutPage", on_delete=models.CASCADE, related_name="team_members")
    photo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="about_team_photo",
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    panels = [
        FieldPanel("photo"),
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("facebook_url"),
        FieldPanel("twitter_url"),
        FieldPanel("youtube_url"),
    ]

    def __str__(self):
        return self.name


class AboutTestimonial(Orderable):
    page = ParentalKey("AboutPage", on_delete=models.CASCADE, related_name="about_testimonials")
    photo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="about_testimonial_photo",
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default="Happy Student")
    quote = models.TextField()

    panels = [
        FieldPanel("photo"),
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("quote"),
    ]

    def __str__(self):
        return self.name


# ──────────────────────────────────────────────
# ABOUT PAGE — FOOTER INLINE MODELS
# ──────────────────────────────────────────────

class AboutFooterSocialLink(Orderable):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("youtube", "YouTube"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
    ]
    page = ParentalKey("AboutPage", on_delete=models.CASCADE, related_name="about_footer_social_links")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    panels = [FieldPanel("platform"), FieldPanel("url")]

    def __str__(self):
        return self.platform


class AboutFooterUsefulLink(Orderable):
    page = ParentalKey("AboutPage", on_delete=models.CASCADE, related_name="about_footer_useful_links")
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label


class AboutFooterExploreLink(Orderable):
    page = ParentalKey("AboutPage", on_delete=models.CASCADE, related_name="about_footer_explore_links")
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label


# ──────────────────────────────────────────────
# CONTACT PAGE — FOOTER INLINE MODELS
# ──────────────────────────────────────────────

class ContactFooterSocialLink(Orderable):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("twitter", "Twitter"),
        ("youtube", "YouTube"),
        ("instagram", "Instagram"),
        ("linkedin", "LinkedIn"),
    ]
    page = ParentalKey("ContactPage", on_delete=models.CASCADE, related_name="contact_footer_social_links")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    panels = [FieldPanel("platform"), FieldPanel("url")]

    def __str__(self):
        return self.platform


class ContactFooterUsefulLink(Orderable):
    page = ParentalKey("ContactPage", on_delete=models.CASCADE, related_name="contact_footer_useful_links")
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label


class ContactFooterExploreLink(Orderable):
    page = ParentalKey("ContactPage", on_delete=models.CASCADE, related_name="contact_footer_explore_links")
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label


# ──────────────────────────────────────────────
# CONTACT PAGE
# ──────────────────────────────────────────────

class ContactPage(Page):

    # ── Navbar ────────────────────────────────
    nav_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="contact_nav_logo",
        verbose_name="Navbar Logo",
    )
    nav_phone = models.CharField(max_length=30, default="", verbose_name="Phone Number")

    # ── Sub-banner ────────────────────────────
    banner_bg_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="contact_banner_bg",
        verbose_name="Banner Background Image",
    )
    banner_title = models.CharField(max_length=200, default="Contact Us")
    banner_description = models.TextField(default="")

    # ── Contact Info section ──────────────────
    contact_info_subtitle = models.CharField(max_length=100, default="Contact Info")
    contact_info_title = models.CharField(max_length=200, default="Our Contact Information")

    # Location box
    location_address = models.TextField(default="")
    location_map_url = models.URLField(blank=True, verbose_name="Location Google Maps URL")

    # Phone box
    phone_1 = models.CharField(max_length=30, default="")
    phone_2 = models.CharField(max_length=30, default="", blank=True)

    # Email box
    email_1 = models.EmailField(default="")
    email_2 = models.EmailField(default="", blank=True)

    # ── Contact Form section ──────────────────
    form_subtitle = models.CharField(max_length=100, default="Registration")
    form_title = models.CharField(max_length=200, default="Register Your Free Account")
    form_bg_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="contact_form_bg",
        verbose_name="Form Left Background Image",
    )

    # ── Map ───────────────────────────────────
    map_embed_url = models.URLField(blank=True, verbose_name="Google Maps Embed URL")

    # ── Footer ────────────────────────────────
    footer_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="contact_footer_logo",
    )
    footer_newsletter_heading = models.CharField(max_length=200, default="Sign up for the newsletter:")
    footer_about_title = models.CharField(max_length=100, default="About Us")
    footer_about_text = models.TextField(default="")
    footer_links_title = models.CharField(max_length=100, default="Useful Links")
    footer_explore_title = models.CharField(max_length=100, default="Explore")
    footer_contact_title = models.CharField(max_length=100, default="Contact Us")
    footer_contact_phone = models.CharField(max_length=30, default="")
    footer_contact_email = models.EmailField(default="")
    footer_contact_address = models.CharField(max_length=300, default="")
    footer_contact_map_url = models.URLField(blank=True)
    footer_copyright_text = models.CharField(max_length=200, default="")

    # ──────────────────────────────────────────
    # ADMIN PANELS
    # ──────────────────────────────────────────

    content_panels = Page.content_panels + [

        MultiFieldPanel([
            FieldPanel("nav_logo"),
            FieldPanel("nav_phone"),
        ], heading="Navbar"),

        MultiFieldPanel([
            FieldPanel("banner_bg_image"),
            FieldPanel("banner_title"),
            FieldPanel("banner_description"),
        ], heading="Sub-Banner"),

        MultiFieldPanel([
            FieldPanel("contact_info_subtitle"),
            FieldPanel("contact_info_title"),
            MultiFieldPanel([
                FieldPanel("location_address"),
                FieldPanel("location_map_url"),
            ], heading="Location Box"),
            MultiFieldPanel([
                FieldRowPanel([FieldPanel("phone_1"), FieldPanel("phone_2")]),
            ], heading="Phone Box"),
            MultiFieldPanel([
                FieldRowPanel([FieldPanel("email_1"), FieldPanel("email_2")]),
            ], heading="Email Box"),
        ], heading="Contact Info Section"),

        MultiFieldPanel([
            FieldPanel("form_subtitle"),
            FieldPanel("form_title"),
            FieldPanel("form_bg_image"),
        ], heading="Contact Form Section"),

        MultiFieldPanel([
            FieldPanel("map_embed_url"),
        ], heading="Map"),

        MultiFieldPanel([
            FieldPanel("footer_logo"),
            FieldPanel("footer_newsletter_heading"),
            FieldPanel("footer_about_title"),
            FieldPanel("footer_about_text"),
            InlinePanel("contact_footer_social_links", label="Social Links"),
            FieldPanel("footer_links_title"),
            InlinePanel("contact_footer_useful_links", label="Useful Links"),
            FieldPanel("footer_explore_title"),
            InlinePanel("contact_footer_explore_links", label="Explore Links"),
            FieldPanel("footer_contact_title"),
            FieldRowPanel([FieldPanel("footer_contact_phone"), FieldPanel("footer_contact_email")]),
            FieldPanel("footer_contact_address"),
            FieldPanel("footer_contact_map_url"),
            FieldPanel("footer_copyright_text"),
        ], heading="Footer"),
    ]

    class Meta:
        verbose_name = "Contact Page"


# ──────────────────────────────────────────────
# ABOUT PAGE
# ──────────────────────────────────────────────

class AboutPage(Page):

    # ── Navbar ────────────────────────────────
    nav_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="about_nav_logo",
        verbose_name="Navbar Logo",
    )
    nav_phone = models.CharField(max_length=30, default="", verbose_name="Phone Number")

    # ── Sub-banner ────────────────────────────
    banner_title = models.CharField(max_length=200, default="About Us")
    banner_description = models.TextField(default="")

    # ── About Section ─────────────────────────
    about_subtitle = models.CharField(max_length=100, default="About Us")
    about_heading = models.CharField(max_length=300, default="")
    about_description = models.TextField(default="")
    about_image1 = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="about_page_image1",
        verbose_name="About Image 1 (main)",
    )
    about_image2 = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="about_page_image2",
        verbose_name="About Image 2 (overlap)",
    )
    about_btn_label = models.CharField(max_length=50, default="Read More")
    about_btn_url = models.CharField(max_length=255, default="./about.html")

    # ── Choose / Features Section ─────────────
    choose_subtitle = models.CharField(max_length=100, default="Our Features")
    choose_heading = models.CharField(max_length=300, default="Why You Should Choose Us")

    # ── Benefit Section ───────────────────────
    benefit_subtitle = models.CharField(max_length=100, default="Our Expertise")
    benefit_heading = models.CharField(max_length=300, default="Benefits of Learning With Us")
    benefit_description = models.TextField(default="")
    benefit_video_thumb = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="about_benefit_video_thumb",
        verbose_name="Benefit Video Background Image",
    )
    benefit_video_url = models.URLField(blank=True, verbose_name="Benefit Video URL")

    # ── Team Section ──────────────────────────
    team_subtitle = models.CharField(max_length=100, default="Instructors")
    team_heading = models.CharField(max_length=300, default="Our Skilled Instructors")

    # ── Testimonials Section ──────────────────
    testimonials_subtitle = models.CharField(max_length=100, default="Reviews")
    testimonials_heading = models.CharField(max_length=300, default="Student's Say About Us")

    # ── Footer ────────────────────────────────
    footer_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="about_footer_logo",
    )
    footer_newsletter_heading = models.CharField(max_length=200, default="Sign up for the newsletter:")
    footer_about_title = models.CharField(max_length=100, default="About Us")
    footer_about_text = models.TextField(default="")
    footer_links_title = models.CharField(max_length=100, default="Useful Links")
    footer_explore_title = models.CharField(max_length=100, default="Explore")
    footer_contact_title = models.CharField(max_length=100, default="Contact Us")
    footer_contact_phone = models.CharField(max_length=30, default="")
    footer_contact_email = models.EmailField(default="")
    footer_contact_address = models.CharField(max_length=300, default="")
    footer_contact_map_url = models.URLField(blank=True)
    footer_copyright_text = models.CharField(max_length=200, default="")

    # ──────────────────────────────────────────
    # ADMIN PANELS
    # ──────────────────────────────────────────

    content_panels = Page.content_panels + [

        MultiFieldPanel([
            FieldPanel("nav_logo"),
            FieldPanel("nav_phone"),
        ], heading="Navbar"),

        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_description"),
        ], heading="Sub-Banner"),

        MultiFieldPanel([
            FieldPanel("about_subtitle"),
            FieldPanel("about_heading"),
            FieldPanel("about_description"),
            FieldPanel("about_image1"),
            FieldPanel("about_image2"),
            FieldRowPanel([FieldPanel("about_btn_label"), FieldPanel("about_btn_url")]),
            InlinePanel("about_features", label="Bullet Points"),
        ], heading="About Section"),

        MultiFieldPanel([
            FieldPanel("choose_subtitle"),
            FieldPanel("choose_heading"),
            InlinePanel("choose_features", label="Feature Boxes"),
        ], heading="Choose / Features Section"),

        MultiFieldPanel([
            FieldPanel("benefit_subtitle"),
            FieldPanel("benefit_heading"),
            FieldPanel("benefit_description"),
            FieldPanel("benefit_video_thumb"),
            FieldPanel("benefit_video_url"),
            InlinePanel("benefit_stats", label="Counter Stats"),
        ], heading="Benefit Section"),

        MultiFieldPanel([
            FieldPanel("team_subtitle"),
            FieldPanel("team_heading"),
            InlinePanel("team_members", label="Team Members"),
        ], heading="Team Section"),

        MultiFieldPanel([
            FieldPanel("testimonials_subtitle"),
            FieldPanel("testimonials_heading"),
            InlinePanel("about_testimonials", label="Testimonials"),
        ], heading="Testimonials Section"),

        MultiFieldPanel([
            FieldPanel("footer_logo"),
            FieldPanel("footer_newsletter_heading"),
            FieldPanel("footer_about_title"),
            FieldPanel("footer_about_text"),
            InlinePanel("about_footer_social_links", label="Social Links"),
            FieldPanel("footer_links_title"),
            InlinePanel("about_footer_useful_links", label="Useful Links"),
            FieldPanel("footer_explore_title"),
            InlinePanel("about_footer_explore_links", label="Explore Links"),
            FieldPanel("footer_contact_title"),
            FieldRowPanel([FieldPanel("footer_contact_phone"), FieldPanel("footer_contact_email")]),
            FieldPanel("footer_contact_address"),
            FieldPanel("footer_contact_map_url"),
            FieldPanel("footer_copyright_text"),
        ], heading="Footer"),
    ]

    class Meta:
        verbose_name = "About Page"


# ──────────────────────────────────────────────
# MAIN HOME PAGE MODEL
# ──────────────────────────────────────────────

class HomePage(Page):

    # ── Navbar ────────────────────────────────
    nav_logo = models.ForeignKey(
        "wagtailimages.Image", null=True,
        on_delete=models.SET_NULL, related_name="nav_logo_image",
        verbose_name="Logo",
    )
    nav_school_name = models.CharField(
        max_length=100, blank=True, default="",
        verbose_name="School Short Name",
        help_text="Short name shown next to the logo, e.g. 'Azeem School'",
    )
    nav_phone = models.CharField(max_length=30, default="", verbose_name="Phone Number")
    nav_btn_label = models.CharField(max_length=50, default="", verbose_name="Button Label")
    nav_btn_url = models.CharField(max_length=255, default="", verbose_name="Button URL")

    # ── Hero ──────────────────────────────────
    hero_bg_image = models.ForeignKey(
        "wagtailimages.Image", null=True,
        on_delete=models.SET_NULL, related_name="hero_bg_image",
        verbose_name="Background Image",
    )
    hero_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="hero_logo_image",
        verbose_name="Hero Logo",
    )
    hero_headline = models.CharField(max_length=300, default="", verbose_name="Headline")
    hero_headline_2 = models.CharField(max_length=300, default="", verbose_name="Headline 2 Optional")
    hero_tagline = models.CharField(max_length=300, default="", verbose_name="Tagline")
    hero_btn_label = models.CharField(max_length=50, default="", verbose_name="Button Title")
    hero_btn_url = models.CharField(max_length=255, default="", verbose_name="Button URL")

    # ── Trust ─────────────────────────────────
    trust_heading = models.CharField(max_length=200, default="", verbose_name="Heading")
    trust_description = models.TextField(default="", verbose_name="Description")
    trust_btn_label = models.CharField(max_length=50, default="", verbose_name="Button Label")
    trust_btn_url = models.CharField(max_length=255, default="", verbose_name="Button URL")

    # ── About ─────────────────────────────────
    about_subtitle = models.CharField(max_length=100, default="")
    about_title = models.CharField(max_length=300, default="")
    about_description = models.TextField(default="")
    about_image_main = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="about_image_main",
    )
    about_image_video_thumb = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="about_image_video_thumb",
    )
    about_video_url = models.URLField(blank=True)
    about_mission_icon = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="about_mission_icon",
    )
    about_mission_title = models.CharField(max_length=300, blank=True)

    # ── Boards ────────────────────────────────
    boards_subtitle = models.CharField(max_length=100, default="Academic Programs")
    boards_title = models.CharField(max_length=300, default="Boards We Follow")
    boards_description = models.TextField(default="We follow the curriculum of top educational boards to ensure quality education for our students.")

    # ── Facilities Teaser ─────────────────────
    facilities_subtitle = models.CharField(
        max_length=100, blank=True, default="Campus Life",
        verbose_name="Section Label",
        help_text='Small label above the heading.  e.g.  Campus Life',
    )
    facilities_title = models.CharField(
        max_length=300, blank=True, default="World-Class Facilities",
        verbose_name="Section Heading",
        help_text='Main heading.  e.g.  World-Class Facilities',
    )
    facilities_description = models.TextField(
        blank=True,
        default="Every resource a student needs — under one roof, in a safe and inspiring environment.",
        verbose_name="Section Description",
        help_text='One or two sentences shown below the heading.',
    )

    # ── Explore Pages toggle ──────────────────
    show_explore_pages = models.BooleanField(
        default=True,
        verbose_name="Show 'Explore Azeem School' section",
        help_text="Tick to display the 6 page-navigation cards (About, Academics, Admissions, Facilities, News, Contact). Untick to hide the section.",
    )

    # ── Courses (kept for migration compatibility) ─
    courses_subtitle = models.CharField(max_length=100, default="")
    courses_title = models.CharField(max_length=300, default="")

    # ── Admissions CTA ────────────────────────
    admissions_cta_subtitle = models.CharField(max_length=100, blank=True, default="Admissions Open")
    admissions_cta_title = models.CharField(max_length=300, blank=True, default="")
    admissions_cta_description = models.TextField(blank=True, default="")
    admissions_cta_btn_label = models.CharField(max_length=50, blank=True, default="Apply Now")
    admissions_cta_btn_url = models.CharField(max_length=255, blank=True, default="")
    admissions_cta_secondary_label = models.CharField(max_length=50, blank=True, default="")
    admissions_cta_secondary_url = models.CharField(max_length=255, blank=True, default="")

    # ── Notices / Announcements ───────────────
    notices_subtitle = models.CharField(max_length=100, default="Latest Updates")
    notices_title = models.CharField(max_length=300, default="School Notices & Announcements")

    # ── Benefits ──────────────────────────────
    benefits_subtitle = models.CharField(max_length=100, default="")
    benefits_title = models.CharField(max_length=300, default="")

    # ── Journey CTA ───────────────────────────
    journey_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="journey_logo_image",
    )
    journey_subtitle = models.CharField(max_length=100, default="")
    journey_title = models.CharField(max_length=300, default="")
    journey_btn_label = models.CharField(max_length=50, default="")
    journey_btn_url = models.CharField(max_length=255, default="")

    # ── Testimonials ──────────────────────────
    testimonials_subtitle = models.CharField(max_length=100, default="")
    testimonials_title = models.CharField(max_length=300, default="")

    # ── Blog / Articles ───────────────────────
    blog_subtitle = models.CharField(max_length=100, default="")
    blog_title = models.CharField(max_length=300, default="")

    # ── Footer ────────────────────────────────
    footer_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="footer_logo_img",
    )
    footer_newsletter_heading = models.CharField(max_length=200, default="")
    footer_about_title = models.CharField(max_length=100, default="About Us")
    footer_about_text = models.TextField(default="")
    footer_links_title = models.CharField(max_length=100, default="Useful Links")
    footer_explore_title = models.CharField(max_length=100, default="Explore")
    footer_contact_title = models.CharField(max_length=100, default="Contact Us")
    footer_contact_phone = models.CharField(max_length=30, default="")
    footer_contact_email = models.EmailField(default="")
    footer_contact_address = models.CharField(max_length=300, default="")
    footer_contact_map_url = models.URLField(blank=True)
    footer_copyright_text = models.CharField(max_length=200, default="")

    # ──────────────────────────────────────────
    # ADMIN PANELS
    # ──────────────────────────────────────────

    content_panels = Page.content_panels + [

        # ── Section 1: Navbar ─────────────────────────────────────────────
        MultiFieldPanel([
            FieldRowPanel([FieldPanel("nav_logo"), FieldPanel("nav_school_name")]),
            FieldPanel("nav_phone"),
            InlinePanel("navbar_menus", label="Menu Items (with Dropdowns)"),
            FieldRowPanel([FieldPanel("nav_btn_label"), FieldPanel("nav_btn_url")]),
        ], heading="① Navbar"),

        # ── Section 2: Hero / Banner ──────────────────────────────────────
        MultiFieldPanel([
            FieldPanel("hero_bg_image"),
            FieldPanel("hero_logo"),
            FieldPanel("hero_headline"),
            FieldPanel("hero_headline_2"),
            FieldPanel("hero_tagline"),
            FieldRowPanel([FieldPanel("hero_btn_label"), FieldPanel("hero_btn_url")]),
        ], heading="② Hero / Banner"),

        # ── Section 3: Stats Strip ────────────────────────────────────────
        MultiFieldPanel([
            InlinePanel("benefit_cards", label="Stat Cards  (counter, suffix %, +, label)"),
        ], heading="③ Stats Strip  — 98%, 500+, 25+, 1500+"),

        # ── Section 4: Why Choose Us ──────────────────────────────────────
        MultiFieldPanel([
            FieldPanel("trust_heading"),
            FieldPanel("trust_description"),
            FieldRowPanel([FieldPanel("trust_btn_label"), FieldPanel("trust_btn_url")]),
            InlinePanel("trust_cards", label="Feature Cards  (icon dropdown, heading, description)"),
        ], heading="④ Why Choose Us"),

        # ── Section 5: About ──────────────────────────────────────────────
        MultiFieldPanel([
            FieldRowPanel([FieldPanel("about_subtitle"), FieldPanel("about_title")]),
            FieldPanel("about_description"),
            FieldPanel("about_image_main"),
            FieldPanel("about_image_video_thumb"),
            FieldPanel("about_video_url",
                       help_text="YouTube URL — used for both the hero 'Watch Our Story' button and the About play button."),
            InlinePanel("about_features", label="Bullet Points  (tick-list items)"),
            FieldRowPanel([FieldPanel("about_mission_icon"), FieldPanel("about_mission_title")]),
        ], heading="⑤ About Us"),

        # ── Section 6: Boards ─────────────────────────────────────────────
        MultiFieldPanel([
            FieldRowPanel([FieldPanel("boards_subtitle"), FieldPanel("boards_title"), FieldPanel("boards_description")]), 
            InlinePanel("board_cards", label="Board Cards  (icon, board name, level, subjects, link)"),
        ], heading="⑥ Boards  — BSEK & Aga Khan"),

        # ── Section 7: Facilities Teaser ─────────────────────────────────
        MultiFieldPanel([
            FieldRowPanel([FieldPanel("facilities_subtitle"), FieldPanel("facilities_title")]),
            FieldPanel("facilities_description"),
            InlinePanel("facility_teasers", label="Facility Cards  (image, icon, title, description, link)"),
        ], heading="⑦ Facilities Teaser  — 4 cards recommended"),

        # ── Section 7b: Explore Pages toggle ─────────────────────────────
        MultiFieldPanel([
            FieldPanel("show_explore_pages"),
        ], heading="⑦b Explore Pages  — toggle on/off"),

        # ── Section 8: Admissions CTA ─────────────────────────────────────
        MultiFieldPanel([
            FieldPanel("admissions_cta_subtitle",
                       help_text="Small badge text, e.g. 'Admissions Open'"),
            FieldPanel("admissions_cta_title"),
            FieldPanel("admissions_cta_description"),
            FieldRowPanel([FieldPanel("admissions_cta_btn_label"), FieldPanel("admissions_cta_btn_url")]),
            FieldRowPanel([FieldPanel("admissions_cta_secondary_label"), FieldPanel("admissions_cta_secondary_url")]),
        ], heading="⑧ Admissions CTA  — also used in footer strip"),

        # ── Section 9: Testimonials ───────────────────────────────────────
        MultiFieldPanel([
            FieldRowPanel([FieldPanel("testimonials_subtitle"), FieldPanel("testimonials_title")]),
            InlinePanel("testimonials", label="Testimonials  (quote, photo, name, role)"),
        ], heading="⑨ Testimonials"),

        # ── Section 9: Notices / Announcements ───────────────────────────
        MultiFieldPanel([
            FieldRowPanel([FieldPanel("notices_subtitle"), FieldPanel("notices_title")]),
            InlinePanel("home_notices", label="Notices  (icon, title, description, date, URL, urgent flag)"),
        ], heading="⑩ Notices & Announcements"),

        # ── Section 10: Footer ────────────────────────────────────────────
        MultiFieldPanel([
            FieldPanel("footer_logo"),
            FieldPanel("footer_about_title"),
            FieldPanel("footer_about_text"),
            InlinePanel("footer_social_links", label="Social Links"),
            FieldRowPanel([FieldPanel("footer_links_title"), FieldPanel("footer_explore_title")]),
            InlinePanel("footer_useful_links", label="Useful Links"),
            InlinePanel("footer_explore_links", label="Explore / Programs Links"),
            FieldPanel("footer_contact_title"),
            FieldRowPanel([FieldPanel("footer_contact_phone"), FieldPanel("footer_contact_email")]),
            FieldPanel("footer_contact_address"),
            FieldPanel("footer_contact_map_url"),
            FieldPanel("footer_copyright_text"),
        ], heading="⑪ Footer"),
    ]

    class Meta:
        verbose_name = "Home Page"


# ──────────────────────────────────────────────
# ACADEMICS PAGE — SHARED CHOICES
# ──────────────────────────────────────────────

ACAD_ICON_CHOICES = [
    # Education & Subjects
    ("fa-solid fa-graduation-cap",  "Graduation Cap"),
    ("fa-solid fa-book",            "Book (closed)"),
    ("fa-solid fa-book-open",       "Book (open)"),
    ("fa-solid fa-book-open-reader","Book Reader"),
    ("fa-solid fa-calculator",      "Calculator / Maths"),
    ("fa-solid fa-flask",           "Flask / Chemistry"),
    ("fa-solid fa-microscope",      "Microscope / Science"),
    ("fa-solid fa-atom",            "Atom / Physics"),
    ("fa-solid fa-dna",             "DNA / Biology"),
    ("fa-solid fa-bolt",            "Bolt / Electricity"),
    ("fa-solid fa-computer",        "Computer / IT"),
    ("fa-solid fa-language",        "Language / English"),
    ("fa-solid fa-pen-nib",         "Pen / Urdu Writing"),
    ("fa-solid fa-pen-to-square",   "Edit / Exam"),
    ("fa-solid fa-palette",         "Art & Craft"),
    ("fa-solid fa-map",             "Map / Social Studies"),
    ("fa-solid fa-flag",            "Flag / Pakistan Studies"),
    ("fa-solid fa-moon",            "Moon / Islamic Studies"),
    ("fa-solid fa-seedling",        "Seedling / Early Years"),
    ("fa-solid fa-person-running",  "Physical Education"),
    ("fa-solid fa-heart",           "Heart / Moral Education"),
    ("fa-solid fa-earth-asia",      "Globe / General Knowledge"),
    # Achievement
    ("fa-solid fa-trophy",          "Trophy"),
    ("fa-solid fa-medal",           "Medal"),
    ("fa-solid fa-star",            "Star"),
    ("fa-solid fa-award",           "Award / Certificate"),
    # Assessment & Files
    ("fa-solid fa-clipboard-check", "Clipboard Check"),
    ("fa-solid fa-file-pen",        "File Pen / Test"),
    ("fa-solid fa-file-invoice",    "File / Document"),
    ("fa-solid fa-list-check",      "List / Book List"),
    ("fa-solid fa-file-arrow-down", "File Download"),
    ("fa-regular fa-calendar",      "Calendar"),
    # Calendar seasons
    ("fa-solid fa-leaf",            "Leaf / Autumn Term"),
    ("fa-solid fa-snowflake",       "Snowflake / Winter"),
    ("fa-solid fa-sun",             "Sun / Summer"),
    # General
    ("fa-solid fa-check",           "Checkmark"),
    ("fa-solid fa-lightbulb",       "Lightbulb / Idea"),
    ("fa-solid fa-users",           "Users / Group"),
    ("fa-solid fa-chalkboard-user", "Teacher"),
    ("fa-solid fa-school",          "School Building"),
]

# For icons on WHITE / LIGHT backgrounds (subjects, downloads, assessments)
ACAD_COLOR_CHOICES = [
    ("icon-blue",   "Blue"),
    ("icon-green",  "Green"),
    ("icon-yellow", "Yellow / Amber"),
    ("icon-pink",   "Pink / Red"),
    ("icon-purple", "Purple"),
    ("icon-cyan",   "Cyan / Teal"),
    ("icon-orange", "Orange"),
    ("icon-dark",   "Dark Navy + Accent"),
]

# For icons on DARK NAVY background (grade ladder panel)
ACAD_GL_COLOR_CHOICES = [
    ("gl-accent", "Lime / Accent"),
    ("gl-blue",   "Blue / Purple"),
    ("gl-green",  "Green"),
    ("gl-yellow", "Yellow"),
    ("gl-pink",   "Pink"),
    ("gl-purple", "Violet"),
    ("gl-cyan",   "Cyan"),
]

ACAD_LEVEL_CHOICES = [
    ("early_years", "Early Years (Pre-Mon, Mon, KG1, KG2)"),
    ("primary",     "Primary (Class 1–5)"),
    ("middle",      "Middle (Class 6–8)"),
    ("secondary",   "Secondary (Class 9–10)"),
]

ACAD_AVATAR_COLOR_CHOICES = [
    ("#6a52e0", "Purple"),
    ("#52b788", "Green"),
    ("#f4b942", "Yellow / Amber"),
    ("#ec407a", "Pink"),
    ("#ab47bc", "Violet"),
    ("#26c6da", "Cyan"),
    ("#42a5f5", "Blue"),
    ("#ff7043", "Orange"),
    ("#1f1741", "Dark Navy"),
]


# ──────────────────────────────────────────────
# ACADEMICS PAGE — INLINE MODELS
# ──────────────────────────────────────────────

class AcademicStat(Orderable):
    page = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="academic_stats")
    number = models.CharField(max_length=20, default="14",
                              help_text='e.g. "14", "98", "25"')
    suffix = models.CharField(max_length=10, blank=True, default="+",
                              help_text='e.g. "+", "%", "×"')
    label  = models.CharField(max_length=150, default="Subjects Offered")

    panels = [
        FieldRowPanel([FieldPanel("number"), FieldPanel("suffix")]),
        FieldPanel("label"),
    ]

    def __str__(self):
        return f"{self.number}{self.suffix} — {self.label}"


class AcademicBoard(Orderable):
    BORDER_CHOICES = [
        ("soft-blue", "Soft Blue (primary)"),
        ("accent",    "Lime / Accent (highlight)"),
    ]

    page        = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="academic_boards")
    border_color = models.CharField(max_length=20, choices=BORDER_CHOICES, default="soft-blue",
                                    help_text="Left border colour of this board card")
    icon_bg_dark = models.BooleanField(default=False,
                                       help_text="Tick for dark-navy icon background instead of soft-blue")
    icon_choice = models.CharField(max_length=100, choices=ACAD_ICON_CHOICES,
                                   default="fa-solid fa-graduation-cap")
    name        = models.CharField(max_length=200, default="Board Name")
    description = models.TextField(default="")
    tag_1       = models.CharField(max_length=100, blank=True, default="",
                                   help_text="Grade / group tag (optional)")
    tag_2       = models.CharField(max_length=100, blank=True, default="",
                                   help_text="Grade / group tag (optional)")
    tag_3       = models.CharField(max_length=100, blank=True, default="",
                                   help_text="Grade / group tag (optional)")

    panels = [
        FieldRowPanel([FieldPanel("border_color"), FieldPanel("icon_bg_dark")]),
        FieldPanel("icon_choice"),
        FieldPanel("name"),
        FieldPanel("description"),
        FieldRowPanel([FieldPanel("tag_1"), FieldPanel("tag_2"), FieldPanel("tag_3")]),
    ]

    def __str__(self):
        return self.name


class AcademicGradeLadderItem(Orderable):
    page       = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="grade_ladder_items")
    icon_choice = models.CharField(max_length=100, choices=ACAD_ICON_CHOICES,
                                   default="fa-solid fa-book-open")
    icon_color = models.CharField(max_length=20, choices=ACAD_GL_COLOR_CHOICES, default="gl-blue",
                                  help_text="Icon colour on dark-navy background")
    title      = models.CharField(max_length=100, default="Grade Level")
    subtitle   = models.CharField(max_length=200, default="",
                                  help_text='e.g. "Class 1 – Class 5"')

    panels = [
        FieldRowPanel([FieldPanel("icon_choice"), FieldPanel("icon_color")]),
        FieldPanel("title"),
        FieldPanel("subtitle"),
    ]

    def __str__(self):
        return self.title


class AcademicSubject(Orderable):
    page       = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="academic_subjects")
    level      = models.CharField(max_length=20, choices=ACAD_LEVEL_CHOICES, default="primary")
    name       = models.CharField(max_length=100, default="Subject")
    icon_choice = models.CharField(max_length=100, choices=ACAD_ICON_CHOICES,
                                   default="fa-solid fa-book")
    icon_color = models.CharField(max_length=20, choices=ACAD_COLOR_CHOICES, default="icon-blue")

    panels = [
        FieldPanel("level"),
        FieldPanel("name"),
        FieldRowPanel([FieldPanel("icon_choice"), FieldPanel("icon_color")]),
    ]

    def __str__(self):
        return f"{self.get_level_display()} — {self.name}"


class AcademicCalendarTerm(Orderable):
    page            = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="calendar_terms")
    badge_label     = models.CharField(max_length=50, default="Term 1",
                                       help_text='Lime badge label, e.g. "Term 1", "Break", "Finals"')
    badge_icon_choice = models.CharField(max_length=100, choices=ACAD_ICON_CHOICES,
                                         default="fa-solid fa-leaf")
    title           = models.CharField(max_length=100, default="Autumn Term")
    date_range      = models.CharField(max_length=100, default="Sep 2 – Nov 15")
    events          = models.TextField(
        default="",
        help_text="One event per line, e.g.:\nSchool reopens — Sep 2\nUnit Test 1 — Oct 4",
    )

    panels = [
        FieldRowPanel([FieldPanel("badge_label"), FieldPanel("badge_icon_choice")]),
        FieldPanel("title"),
        FieldPanel("date_range"),
        FieldPanel("events"),
    ]

    @property
    def events_list(self):
        return [e.strip() for e in self.events.splitlines() if e.strip()]

    def __str__(self):
        return self.title


class AcademicAssessment(Orderable):
    page       = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="academic_assessments")
    icon_choice = models.CharField(max_length=100, choices=ACAD_ICON_CHOICES,
                                   default="fa-solid fa-clipboard-check")
    icon_color = models.CharField(max_length=20, choices=ACAD_COLOR_CHOICES, default="icon-blue")
    title      = models.CharField(max_length=200, default="Assessment Type")
    description = models.TextField(default="")
    weight     = models.CharField(max_length=20, default="20%",
                                  help_text='Weightage badge text, e.g. "20% Weightage"')

    panels = [
        FieldRowPanel([FieldPanel("icon_choice"), FieldPanel("icon_color")]),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("weight"),
    ]

    def __str__(self):
        return self.title


class AcademicFaculty(Orderable):
    page           = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="academic_faculty")
    name           = models.CharField(max_length=100, default="Faculty Name")
    subject        = models.CharField(max_length=100, default="Subject")
    experience     = models.CharField(max_length=50, blank=True, default="",
                                      help_text='e.g. "10 yrs experience"')
    avatar_initial = models.CharField(max_length=2, default="A",
                                      help_text="1–2 letters displayed in the avatar circle")
    avatar_color   = models.CharField(max_length=20, choices=ACAD_AVATAR_COLOR_CHOICES, default="#6a52e0",
                                      help_text="Avatar circle background colour")
    is_hod         = models.BooleanField(default=False, verbose_name="Head of Department (HOD)")

    panels = [
        FieldPanel("name"),
        FieldPanel("subject"),
        FieldPanel("experience"),
        FieldRowPanel([FieldPanel("avatar_initial"), FieldPanel("avatar_color")]),
        FieldPanel("is_hod"),
    ]

    def __str__(self):
        return self.name


class AcademicAchievementStat(Orderable):
    page   = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="achievement_stats")
    number = models.CharField(max_length=20, default="98")
    suffix = models.CharField(max_length=10, blank=True, default="%",
                              help_text='e.g. "%", "+", "×"')
    label  = models.CharField(max_length=150, default="Overall Pass Rate")

    panels = [
        FieldRowPanel([FieldPanel("number"), FieldPanel("suffix")]),
        FieldPanel("label"),
    ]

    def __str__(self):
        return f"{self.number}{self.suffix} — {self.label}"


class AcademicAchievementCard(Orderable):
    page        = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="achievement_cards")
    icon_choice = models.CharField(max_length=100, choices=ACAD_ICON_CHOICES, default="fa-solid fa-trophy")
    title       = models.CharField(max_length=200, default="Achievement Highlight")
    description = models.TextField(default="")

    panels = [
        FieldPanel("icon_choice"),
        FieldPanel("title"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.title


class AcademicDownload(Orderable):
    page        = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="academic_downloads")
    icon_choice = models.CharField(max_length=100, choices=ACAD_ICON_CHOICES,
                                   default="fa-solid fa-file-arrow-down")
    icon_color  = models.CharField(max_length=20, choices=ACAD_COLOR_CHOICES, default="icon-blue")
    title       = models.CharField(max_length=200, default="Document Title")
    description = models.CharField(max_length=200, default="PDF · 1 MB",
                                   help_text='e.g. "Complete syllabus for all classes · PDF · 1.2 MB"')
    document    = models.FileField(
        upload_to="documents",
        storage=RawMediaCloudinaryStorage(),
        null=True, blank=True,
        verbose_name="File",
        help_text="Upload a PDF or any file. Visitors will download it on click.",
    )

    panels = [
        FieldRowPanel([FieldPanel("icon_choice"), FieldPanel("icon_color")]),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("document"),
    ]

    def __str__(self):
        return self.title


class AcademicsFooterSocialLink(Orderable):
    PLATFORM_CHOICES = [
        ("facebook",  "Facebook"),
        ("twitter",   "Twitter / X"),
        ("youtube",   "YouTube"),
        ("instagram", "Instagram"),
        ("linkedin",  "LinkedIn"),
    ]
    page     = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="academics_footer_social_links")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url      = models.URLField()
    panels   = [FieldPanel("platform"), FieldPanel("url")]

    def __str__(self):
        return self.platform


class AcademicsFooterUsefulLink(Orderable):
    page   = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="academics_footer_useful_links")
    label  = models.CharField(max_length=100)
    url    = models.CharField(max_length=255)
    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label


class AcademicsFooterExploreLink(Orderable):
    page   = ParentalKey("AcademicsPage", on_delete=models.CASCADE, related_name="academics_footer_explore_links")
    label  = models.CharField(max_length=100)
    url    = models.CharField(max_length=255)
    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label


# ──────────────────────────────────────────────
# ACADEMICS PAGE
# ──────────────────────────────────────────────

class AcademicsPage(Page):

    # ── Navbar ────────────────────────────────
    nav_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="academics_nav_logo",
        verbose_name="Navbar Logo",
    )
    nav_phone       = models.CharField(max_length=30, default="+92 21 3456 7890")
    nav_login_label = models.CharField(max_length=50, default="Student Portal")
    nav_login_url   = models.CharField(max_length=255, default="#")

    # ── Sub-Banner ────────────────────────────
    banner_bg_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="academics_banner_bg",
        verbose_name="Banner Background Image",
        help_text="Recommended resolution: 1920 × 486 px",
    )
    banner_title       = models.CharField(max_length=200, default="Academics")
    banner_description = models.TextField(
        default="Shaping minds with a structured curriculum, dedicated faculty, and a culture of academic excellence.")

    # ── Curriculum Section ────────────────────
    curriculum_subtitle    = models.CharField(max_length=100, default="Curriculum & Board")
    curriculum_heading     = models.CharField(max_length=300, default="A Structured Path to Excellence")
    curriculum_description = models.TextField(
        default="Our curriculum aligns with Pakistan's leading examination boards, ensuring every student is prepared for national and international standards.")
    grade_ladder_subtitle = models.CharField(max_length=100, default="Grade Structure")
    grade_ladder_heading  = models.CharField(max_length=200, default="From First Steps to Board Exams")

    # ── Subjects Section ──────────────────────
    subjects_subtitle    = models.CharField(max_length=100, default="Subjects")
    subjects_heading     = models.CharField(max_length=300, default="What Your Child Will Learn")
    subjects_description = models.TextField(
        default="Select a level to explore the subjects taught at each stage of your child's academic journey.")

    # ── Calendar Section ──────────────────────
    calendar_subtitle    = models.CharField(max_length=100, default="Academic Year 2024–25")
    calendar_heading     = models.CharField(max_length=300, default="Academic Calendar")
    calendar_description = models.TextField(
        default="Plan ahead with every term, examination period, and holiday mapped out for the full academic year.")

    # ── Assessments Section ───────────────────
    assessments_subtitle    = models.CharField(max_length=100, default="Assessments")
    assessments_heading     = models.CharField(max_length=300, default="How We Evaluate Progress")
    assessments_description = models.TextField(
        default="Our multi-layered assessment system ensures every student's growth is measured fairly, comprehensively, and continuously throughout the year.")

    # ── Faculty Section ───────────────────────
    faculty_subtitle    = models.CharField(max_length=100, default="Our Educators")
    faculty_heading     = models.CharField(max_length=300, default="Meet the Faculty")
    faculty_description = models.TextField(
        default="Our qualified and passionate educators bring decades of combined experience to every classroom.")

    # ── Achievements Section ──────────────────
    achievements_subtitle    = models.CharField(max_length=100, default="Results & Achievements")
    achievements_heading     = models.CharField(max_length=300, default="A Proven Track Record")
    achievements_description = models.TextField(
        default="Year after year, our students achieve outstanding results in board examinations and national competitions.")

    # ── Downloads Section ─────────────────────
    downloads_subtitle    = models.CharField(max_length=100, default="Resources")
    downloads_heading     = models.CharField(max_length=300, default="Downloads & Resources")
    downloads_description = models.TextField(
        default="Access official documents, syllabi, forms, and schedules — all in one place.")

    # ── CTA Section ───────────────────────────
    cta_heading      = models.CharField(max_length=200, default="Ready to Enrol Your Child?")
    cta_text         = models.TextField(
        default="Join hundreds of families who trust Azeem School for a world-class education. Apply today and secure your child's place.")
    cta_button_label = models.CharField(max_length=100, default="Apply for Admission")
    cta_button_url   = models.CharField(max_length=255, default="/admissions/")

    # ── Footer ────────────────────────────────
    footer_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="academics_footer_logo",
    )
    footer_newsletter_heading = models.CharField(max_length=200, default="Subscribe to Our Newsletter")
    footer_about_title        = models.CharField(max_length=100, default="About Azeem School")
    footer_about_text         = models.TextField(
        default="Providing quality education with modern teaching methods and a nurturing environment for over 25 years in Karachi.")
    footer_links_title        = models.CharField(max_length=100, default="Quick Links")
    footer_explore_title      = models.CharField(max_length=100, default="Academics")
    footer_contact_title      = models.CharField(max_length=100, default="Contact Us")
    footer_contact_phone      = models.CharField(max_length=30, default="+92 21 3456 7890")
    footer_contact_email      = models.EmailField(default="info@azeem.edu.pk")
    footer_contact_address    = models.CharField(max_length=300, default="KDA Scheme, Karachi, Pakistan")
    footer_contact_map_url    = models.URLField(blank=True)
    footer_copyright_text     = models.CharField(max_length=200, default="© 2025 Azeem School. All Rights Reserved.")

    # ──────────────────────────────────────────
    # ADMIN PANELS
    # ──────────────────────────────────────────

    content_panels = Page.content_panels + [

        MultiFieldPanel([
            FieldPanel("nav_logo"),
            FieldPanel("nav_phone"),
            FieldRowPanel([FieldPanel("nav_login_label"), FieldPanel("nav_login_url")]),
        ], heading="Navbar"),

        MultiFieldPanel([
            FieldPanel("banner_bg_image"),
            FieldPanel("banner_title"),
            FieldPanel("banner_description"),
        ], heading="Sub-Banner"),

        MultiFieldPanel([
            InlinePanel("academic_stats", label="Stat Items"),
        ], heading="Stats Strip"),

        MultiFieldPanel([
            FieldPanel("curriculum_subtitle"),
            FieldPanel("curriculum_heading"),
            FieldPanel("curriculum_description"),
            InlinePanel("academic_boards", label="Board Affiliation Cards"),
            FieldRowPanel([FieldPanel("grade_ladder_subtitle"), FieldPanel("grade_ladder_heading")]),
            InlinePanel("grade_ladder_items", label="Grade Ladder Items"),
        ], heading="Curriculum & Board Section"),

        MultiFieldPanel([
            FieldPanel("subjects_subtitle"),
            FieldPanel("subjects_heading"),
            FieldPanel("subjects_description"),
            InlinePanel("academic_subjects", label="Subjects (grouped by level via the Level field)"),
        ], heading="Subjects Section"),

        MultiFieldPanel([
            FieldPanel("calendar_subtitle"),
            FieldPanel("calendar_heading"),
            FieldPanel("calendar_description"),
            InlinePanel("calendar_terms", label="Calendar Terms / Periods"),
        ], heading="Academic Calendar Section"),

        MultiFieldPanel([
            FieldPanel("assessments_subtitle"),
            FieldPanel("assessments_heading"),
            FieldPanel("assessments_description"),
            InlinePanel("academic_assessments", label="Assessment Cards"),
        ], heading="Assessments Section"),

        MultiFieldPanel([
            FieldPanel("faculty_subtitle"),
            FieldPanel("faculty_heading"),
            FieldPanel("faculty_description"),
            InlinePanel("academic_faculty", label="Faculty Members"),
        ], heading="Faculty Section"),

        MultiFieldPanel([
            FieldPanel("achievements_subtitle"),
            FieldPanel("achievements_heading"),
            FieldPanel("achievements_description"),
            InlinePanel("achievement_stats", label="Achievement Stats"),
            InlinePanel("achievement_cards", label="Achievement Highlight Cards"),
        ], heading="Results & Achievements Section"),

        MultiFieldPanel([
            FieldPanel("downloads_subtitle"),
            FieldPanel("downloads_heading"),
            FieldPanel("downloads_description"),
            InlinePanel("academic_downloads", label="Download Items"),
        ], heading="Downloads Section"),

        MultiFieldPanel([
            FieldPanel("cta_heading"),
            FieldPanel("cta_text"),
            FieldRowPanel([FieldPanel("cta_button_label"), FieldPanel("cta_button_url")]),
        ], heading="CTA Section"),

        MultiFieldPanel([
            FieldPanel("footer_logo"),
            FieldPanel("footer_newsletter_heading"),
            FieldPanel("footer_about_title"),
            FieldPanel("footer_about_text"),
            InlinePanel("academics_footer_social_links", label="Social Links"),
            FieldPanel("footer_links_title"),
            InlinePanel("academics_footer_useful_links", label="Useful Links"),
            FieldPanel("footer_explore_title"),
            InlinePanel("academics_footer_explore_links", label="Explore / Academics Links"),
            FieldPanel("footer_contact_title"),
            FieldRowPanel([FieldPanel("footer_contact_phone"), FieldPanel("footer_contact_email")]),
            FieldPanel("footer_contact_address"),
            FieldPanel("footer_contact_map_url"),
            FieldPanel("footer_copyright_text"),
        ], heading="Footer"),
    ]

    class Meta:
        verbose_name = "Academics Page"


# ══════════════════════════════════════════════════════════════════
# FACILITIES PAGE — SHARED CHOICES
# ══════════════════════════════════════════════════════════════════

FAC_ICON_CHOICES = [
    # Labs & Science
    ("fa-solid fa-atom",                     "Atom / Physics"),
    ("fa-solid fa-flask",                    "Flask / Chemistry"),
    ("fa-solid fa-flask-vial",               "Flask Vial"),
    ("fa-solid fa-dna",                      "DNA / Biology"),
    ("fa-solid fa-microscope",               "Microscope"),
    ("fa-solid fa-laptop-code",              "Laptop Code / Computer"),
    ("fa-solid fa-computer",                 "Computer / IT"),
    ("fa-solid fa-microchip",                "Microchip / Robotics"),
    ("fa-solid fa-robot",                    "Robot / STEM"),
    ("fa-solid fa-language",                 "Language Lab"),
    ("fa-solid fa-print",                    "3D Printer / Print"),
    # Sports
    ("fa-solid fa-futbol",                   "Football"),
    ("fa-solid fa-basketball",               "Basketball"),
    ("fa-solid fa-person-running",           "Athletics / Running"),
    ("fa-solid fa-table-tennis-paddle-ball", "Table Tennis"),
    ("fa-solid fa-dumbbell",                 "Gym / Weights"),
    ("fa-solid fa-water",                    "Swimming Pool"),
    # Library & Resources
    ("fa-solid fa-book-open",                "Book Open"),
    ("fa-solid fa-book",                     "Book"),
    ("fa-solid fa-tablet-screen-button",     "Digital / Tablet"),
    ("fa-solid fa-users",                    "Group / Team"),
    ("fa-solid fa-mug-saucer",               "Lounge / Reading"),
    # Arts & Media
    ("fa-solid fa-music",                    "Music"),
    ("fa-solid fa-palette",                  "Art / Painting"),
    ("fa-solid fa-masks-theater",            "Drama / Theatre"),
    ("fa-solid fa-video",                    "Media / Video"),
    ("fa-solid fa-microphone",               "Microphone / Podcast"),
    # Safety & Welfare
    ("fa-solid fa-shield-halved",            "Shield / Security"),
    ("fa-solid fa-kit-medical",              "Medical / First Aid"),
    ("fa-solid fa-fire-extinguisher",        "Fire Safety"),
    ("fa-solid fa-bus",                      "Transport / Bus"),
    ("fa-solid fa-utensils",                 "Cafeteria / Food"),
    ("fa-solid fa-person-praying",           "Prayer Room"),
    ("fa-solid fa-camera",                   "CCTV / Camera"),
    ("fa-solid fa-heart-pulse",              "Health / Pulse"),
    # General
    ("fa-solid fa-school",                   "School Building"),
    ("fa-solid fa-graduation-cap",           "Graduation Cap"),
    ("fa-solid fa-trophy",                   "Trophy"),
    ("fa-solid fa-star",                     "Star"),
    ("fa-solid fa-check",                    "Checkmark"),
    ("fa-solid fa-circle-check",             "Circle Check"),
    ("fa-solid fa-arrow-right",              "Arrow Right"),
    ("fa-solid fa-lightbulb",                "Lightbulb / Idea"),
]

# Gradient fallback for image cards (value = CSS two-stop gradient)
FAC_GRADIENT_CHOICES = [
    ("#1f1741,#6a52e0",   "Navy → Purple"),
    ("#0d3b2e,#26a69a",   "Dark Green → Teal"),
    ("#0a3d62,#1565c0",   "Dark → Blue"),
    ("#4a0040,#ab47bc",   "Dark → Violet"),
    ("#1a1a2e,#e65100",   "Dark → Orange"),
    ("#003d1f,#2e7d32",   "Dark → Green"),
    ("#1f1741,#ec407a",   "Navy → Pink"),
    ("#1a1a2e,#26c6da",   "Dark → Cyan"),
    ("#1a1a1a,#f4b942",   "Dark → Yellow"),
    ("#1f1741,#42a5f5",   "Navy → Blue"),
]

# Coloured overlay gradient on image tops (lab cards, arts cards)
FAC_OVERLAY_CHOICES = [
    ("rgba(66,165,245,0.75),rgba(31,23,65,0.55)",    "Blue"),
    ("rgba(102,187,106,0.75),rgba(31,23,65,0.55)",   "Green"),
    ("rgba(38,166,154,0.75),rgba(31,23,65,0.55)",    "Teal"),
    ("rgba(171,71,188,0.75),rgba(31,23,65,0.55)",    "Purple"),
    ("rgba(255,112,67,0.75),rgba(31,23,65,0.55)",    "Orange"),
    ("rgba(244,185,66,0.75),rgba(31,23,65,0.55)",    "Yellow"),
    ("rgba(236,64,122,0.75),rgba(31,23,65,0.55)",    "Pink"),
    ("rgba(38,198,218,0.75),rgba(31,23,65,0.55)",    "Cyan"),
]

# Hex colour for the floating icon pill on image cards
FAC_ICON_HEX_CHOICES = [
    ("#42a5f5", "Blue"),
    ("#66bb6a", "Green"),
    ("#26a69a", "Teal"),
    ("#ab47bc", "Purple"),
    ("#ff7043", "Orange"),
    ("#f4b942", "Yellow"),
    ("#ec407a", "Pink"),
    ("#26c6da", "Cyan"),
    ("#1f1741", "Dark Navy"),
]

# Light-background icon colour (library features, safety)
FAC_LIGHT_COLOR_CHOICES = [
    ("icon-blue",   "Blue"),
    ("icon-green",  "Green"),
    ("icon-teal",   "Teal"),
    ("icon-purple", "Purple"),
    ("icon-orange", "Orange"),
    ("icon-yellow", "Yellow"),
    ("icon-pink",   "Pink"),
    ("icon-cyan",   "Cyan"),
]


# ══════════════════════════════════════════════════════════════════
# FACILITIES PAGE — INLINE MODELS
# ══════════════════════════════════════════════════════════════════

class FacilityStat(Orderable):
    page   = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="facility_stats")
    number = models.CharField(max_length=20, default="50",
                              help_text='Numeric value, e.g. "50", "12", "25"')
    suffix = models.CharField(max_length=10, blank=True, default="K",
                              help_text='Unit suffix, e.g. "K", "+", "K+", "%"')
    label  = models.CharField(max_length=150, default="Square Feet Campus")

    panels = [
        FieldRowPanel([FieldPanel("number"), FieldPanel("suffix")]),
        FieldPanel("label"),
    ]

    def __str__(self):
        return f"{self.number}{self.suffix} — {self.label}"


class FacilityOverviewTile(Orderable):
    page        = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="overview_tiles")
    icon_choice = models.CharField(max_length=100, choices=FAC_ICON_CHOICES, default="fa-solid fa-school",
                                   help_text="Font Awesome icon class")
    icon_color  = models.CharField(max_length=20, choices=FAC_LIGHT_COLOR_CHOICES, default="icon-blue",
                                   help_text="Icon background colour theme")
    title       = models.CharField(max_length=100, default="Facility Name")
    description = models.CharField(max_length=250, default="Short description of this facility area.")

    panels = [
        FieldRowPanel([FieldPanel("icon_choice"), FieldPanel("icon_color")]),
        FieldPanel("title"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.title


class FacilityHeroCard(Orderable):
    """Large image card — top two slots in the overview grid."""
    page             = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="facility_hero_cards")
    image            = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="fac_hero_card_image",
        help_text="Main photo for this card (recommended: 800 × 650 px)",
    )
    gradient_fallback = models.CharField(
        max_length=50, choices=FAC_GRADIENT_CHOICES, default="#1f1741,#6a52e0",
        help_text="Gradient shown when no image is uploaded",
    )
    badge_icon  = models.CharField(max_length=100, choices=FAC_ICON_CHOICES, default="fa-solid fa-school",
                                   help_text="Icon inside the lime badge")
    badge_label = models.CharField(max_length=80, default="Facility Name",
                                   help_text='Badge text, e.g. "Science & Labs"')
    title       = models.CharField(max_length=200, default="Facility Title")
    description = models.CharField(max_length=300, default="Short description for this facility area",
                                   help_text="One-line description shown beneath the title")

    panels = [
        FieldPanel("image"),
        FieldPanel("gradient_fallback"),
        FieldRowPanel([FieldPanel("badge_icon"), FieldPanel("badge_label")]),
        FieldPanel("title"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.title


class FacilitySmallCard(Orderable):
    """Smaller image card — bottom four slots in the overview grid."""
    page             = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="facility_small_cards")
    image            = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="fac_small_card_image",
        help_text="Photo for this card (recommended: 500 × 400 px)",
    )
    gradient_fallback = models.CharField(
        max_length=50, choices=FAC_GRADIENT_CHOICES, default="#0a3d62,#1565c0",
        help_text="Gradient shown when no image is uploaded",
    )
    icon_choice = models.CharField(max_length=100, choices=FAC_ICON_CHOICES, default="fa-solid fa-school")
    title       = models.CharField(max_length=100, default="Facility")
    subtitle    = models.CharField(max_length=200, default="Short detail line",
                                   help_text='Short line below title, e.g. "25,000+ volumes"')

    panels = [
        FieldPanel("image"),
        FieldPanel("gradient_fallback"),
        FieldPanel("icon_choice"),
        FieldPanel("title"),
        FieldPanel("subtitle"),
    ]

    def __str__(self):
        return self.title


class FacilityTourBullet(Orderable):
    """Bullet point in the Campus Tour section right panel."""
    page        = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="tour_bullets")
    icon_choice = models.CharField(max_length=100, choices=FAC_ICON_CHOICES, default="fa-solid fa-school")
    title       = models.CharField(max_length=150, default="What You Will See")
    description = models.CharField(max_length=300, default="Brief description of this tour highlight")

    panels = [
        FieldPanel("icon_choice"),
        FieldPanel("title"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.title


class FacilityLab(Orderable):
    page             = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="facility_labs")
    image            = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="fac_lab_image",
        help_text="Lab photo shown at the top of the card (recommended: 700 × 360 px)",
    )
    overlay_color    = models.CharField(
        max_length=100, choices=FAC_OVERLAY_CHOICES,
        default="rgba(66,165,245,0.75),rgba(31,23,65,0.55)",
        help_text="Coloured gradient overlaid on the photo",
    )
    icon_hex_color   = models.CharField(
        max_length=20, choices=FAC_ICON_HEX_CHOICES, default="#42a5f5",
        help_text="Background colour of the floating icon circle",
    )
    icon_choice      = models.CharField(max_length=100, choices=FAC_ICON_CHOICES, default="fa-solid fa-flask")
    icon_color       = models.CharField(max_length=20, choices=FAC_LIGHT_COLOR_CHOICES, default="icon-blue",
                                        help_text="Icon background colour theme")
    title            = models.CharField(max_length=200, default="Lab Name")
    description      = models.TextField(default="Brief description of this laboratory.")
    features         = models.TextField(
        default="Feature one\nFeature two\nFeature three\nCapacity: 30 students",
        help_text="One feature per line. These appear as bullet points.",
    )

    panels = [
        FieldRowPanel([FieldPanel("icon_choice"), FieldPanel("icon_color")]),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("features"),
    ]

    @property
    def features_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]

    def __str__(self):
        return self.title


class FacilitySport(Orderable):
    page    = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="facility_sports")
    image   = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="fac_sport_image",
        help_text="Sport / ground photo (recommended: 600 × 400 px)",
    )
    gradient_fallback = models.CharField(
        max_length=50, choices=FAC_GRADIENT_CHOICES, default="#0d3b2e,#26a69a",
        help_text="Gradient used when no image is uploaded",
    )
    icon_choice = models.CharField(max_length=100, choices=FAC_ICON_CHOICES, default="fa-solid fa-futbol",
                                   help_text="Icon shown at the top of the sport card")
    title       = models.CharField(max_length=200, default="Sport / Facility Name")
    description = models.TextField(default="Brief description of this sports facility.")
    badges      = models.TextField(
        default="Feature One\nFeature Two\nFeature Three",
        help_text="One badge per line, e.g.:\nFloodlit\nFIFA-grade turf\nPavilion",
    )

    panels = [
        FieldPanel("icon_choice"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("badges"),
    ]

    @property
    def badges_list(self):
        return [b.strip() for b in self.badges.splitlines() if b.strip()]

    def __str__(self):
        return self.title


class FacilityLibraryFeature(Orderable):
    page        = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="library_features")
    icon_choice = models.CharField(max_length=100, choices=FAC_ICON_CHOICES, default="fa-solid fa-book-open")
    icon_color  = models.CharField(max_length=20, choices=FAC_LIGHT_COLOR_CHOICES, default="icon-green")
    title       = models.CharField(max_length=200, default="Feature Title")
    description = models.TextField(default="Brief description of this library feature.")

    panels = [
        FieldRowPanel([FieldPanel("icon_choice"), FieldPanel("icon_color")]),
        FieldPanel("title"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.title


class FacilityLibraryStat(Orderable):
    page   = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="library_stats")
    number = models.CharField(max_length=30, default="25K+",
                              help_text='The number displayed, e.g. "25K+", "3,500", "4", "6 AM"')
    label  = models.CharField(max_length=200, default="Books and reference volumes")

    panels = [
        FieldPanel("number"),
        FieldPanel("label"),
    ]

    def __str__(self):
        return f"{self.number} — {self.label}"


class FacilityArtsCard(Orderable):
    page             = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="arts_cards")
    image            = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="fac_arts_card_image",
        help_text="Photo for this arts space (recommended: 500 × 320 px)",
    )
    overlay_color    = models.CharField(
        max_length=100, choices=FAC_OVERLAY_CHOICES,
        default="rgba(236,64,122,0.7),rgba(31,23,65,0.55)",
        help_text="Coloured gradient overlaid on the photo",
    )
    icon_hex_color   = models.CharField(
        max_length=20, choices=FAC_ICON_HEX_CHOICES, default="#ec407a",
        help_text="Background colour of the floating icon circle",
    )
    icon_choice = models.CharField(max_length=100, choices=FAC_ICON_CHOICES, default="fa-solid fa-music")
    icon_color  = models.CharField(max_length=20, choices=FAC_LIGHT_COLOR_CHOICES, default="icon-pink",
                                   help_text="Icon background colour theme")
    title       = models.CharField(max_length=200, default="Arts Space Name")
    description = models.TextField(default="Brief description of this creative space.")
    tags        = models.TextField(
        default="Tag One\nTag Two\nTag Three",
        help_text="One tag per line, e.g.:\nPiano\nGuitar\nDrums",
    )

    panels = [
        FieldRowPanel([FieldPanel("icon_choice"), FieldPanel("icon_color")]),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("tags"),
    ]

    @property
    def tags_list(self):
        return [t.strip() for t in self.tags.splitlines() if t.strip()]

    def __str__(self):
        return self.title


class FacilitySafetyStat(Orderable):
    page   = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="safety_stats")
    number = models.CharField(max_length=20, default="120+",
                              help_text='e.g. "120+", "24/7", "2", "100%"')
    label  = models.CharField(max_length=150, default="CCTV Cameras on Campus")

    panels = [
        FieldRowPanel([FieldPanel("number"), FieldPanel("label")]),
    ]

    def __str__(self):
        return f"{self.number} — {self.label}"


class FacilitySafetyCard(Orderable):
    page        = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="safety_cards")
    icon_choice = models.CharField(max_length=100, choices=FAC_ICON_CHOICES, default="fa-solid fa-shield-halved")
    title       = models.CharField(max_length=200, default="Safety Feature")
    description = models.TextField(default="Description of this safety or welfare provision.")

    panels = [
        FieldPanel("icon_choice"),
        FieldPanel("title"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.title


class FacilityGalleryImage(Orderable):
    page  = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="fac_gallery_image",
        help_text="Campus photo (recommended: 480 × 360 px)",
    )
    alt_text = models.CharField(max_length=200, blank=True, default="",
                                help_text="Optional alt text for accessibility")

    panels = [
        FieldPanel("image"),
        FieldPanel("alt_text"),
    ]

    def __str__(self):
        return self.alt_text or "Gallery Image"


# ── Footer inline models ───────────────────────

class FacilitiesFooterSocialLink(Orderable):
    PLATFORM_CHOICES = [
        ("facebook",  "Facebook"),
        ("twitter",   "Twitter / X"),
        ("youtube",   "YouTube"),
        ("instagram", "Instagram"),
        ("linkedin",  "LinkedIn"),
    ]
    page     = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="facilities_footer_social_links")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url      = models.URLField()
    panels   = [FieldPanel("platform"), FieldPanel("url")]

    def __str__(self):
        return self.platform


class FacilitiesFooterUsefulLink(Orderable):
    page   = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="facilities_footer_useful_links")
    label  = models.CharField(max_length=100)
    url    = models.CharField(max_length=255)
    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label


class FacilitiesFooterExploreLink(Orderable):
    page   = ParentalKey("FacilitiesPage", on_delete=models.CASCADE, related_name="facilities_footer_explore_links")
    label  = models.CharField(max_length=100)
    url    = models.CharField(max_length=255)
    panels = [FieldPanel("label"), FieldPanel("url")]

    def __str__(self):
        return self.label


# ══════════════════════════════════════════════════════════════════
# FACILITIES PAGE
# ══════════════════════════════════════════════════════════════════

class FacilitiesPage(Page):

    # ── Navbar ────────────────────────────────
    nav_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="facilities_nav_logo",
        verbose_name="Navbar Logo",
    )
    nav_phone       = models.CharField(max_length=30, default="+92 21 3456 7890")
    nav_login_label = models.CharField(max_length=50, default="Student Portal")
    nav_login_url   = models.CharField(max_length=255, default="#")

    # ── Sub-Banner ────────────────────────────
    banner_bg_image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="facilities_banner_bg",
        verbose_name="Banner Background Image",
        help_text="Recommended: 1920 × 486 px",
    )
    banner_title       = models.CharField(max_length=200, default="Our Facilities")
    banner_description = models.TextField(
        default="World-class learning environments designed to inspire curiosity, nurture talent, and build tomorrow's leaders.")

    # ── Overview Section ──────────────────────
    overview_subtitle    = models.CharField(max_length=100, default="What We Offer")
    overview_heading     = models.CharField(max_length=300, default="Everything a Modern School Should Have")
    overview_description = models.TextField(
        default="From cutting-edge science labs to open sports arenas, every space at Azeem School is built with purpose.")

    # ── Campus Tour Section ───────────────────
    tour_eyebrow     = models.CharField(max_length=100, default="Virtual Campus Tour")
    tour_heading     = models.CharField(max_length=300, default="See Every Corner of Our Campus")
    tour_description = models.TextField(
        default="Walk through our labs, sports grounds, library, arts spaces, and more — from wherever you are.")
    tour_youtube_url = models.URLField(
        blank=True, default="",
        verbose_name="YouTube Embed URL",
        help_text=(
            "Paste the full YouTube embed URL, e.g. https://www.youtube.com/embed/YOUR_VIDEO_ID "
            "Leave blank to show the 'Coming Soon' placeholder."
        ),
    )
    tour_placeholder_bg = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="facilities_tour_placeholder_bg",
        verbose_name="Tour Placeholder Background Image",
        help_text="Background photo shown behind the play button while the video URL is not set",
    )
    tour_btn_label = models.CharField(max_length=100, default="Book a Live Campus Visit")
    tour_btn_url   = models.CharField(max_length=255, default="/contact/")

    # ── Labs Section ──────────────────────────
    labs_subtitle    = models.CharField(max_length=100, default="Hands-On Learning")
    labs_heading     = models.CharField(max_length=300, default="State-of-the-Art Laboratories")
    labs_description = models.TextField(
        default="Purpose-built labs that turn textbook theory into real-world discovery for every grade level.")

    # ── Sports Section ────────────────────────
    sports_subtitle    = models.CharField(max_length=100, default="Active & Healthy")
    sports_heading     = models.CharField(max_length=300, default="Sports & Athletics Facilities")
    sports_description = models.TextField(
        default="We believe every student deserves a healthy body alongside a sharp mind. Our sports infrastructure reflects that commitment.")

    # ── Library Section ───────────────────────
    library_subtitle      = models.CharField(max_length=100, default="Knowledge Hub")
    library_heading       = models.CharField(max_length=300, default="Library & Resource Centre")
    library_description   = models.TextField(
        default="A quiet, inspiring space that fuels independent research, reading habits, and lifelong learning.")
    library_panel_eyebrow = models.CharField(max_length=100, default="Library at a Glance")
    library_panel_heading = models.CharField(max_length=200, default="A World of Knowledge, One Shelf Away")

    # ── Arts Section ──────────────────────────
    arts_subtitle    = models.CharField(max_length=100, default="Creative Expression")
    arts_heading     = models.CharField(max_length=300, default="Arts & Performing Arts Spaces")
    arts_description = models.TextField(
        default="Dedicated spaces for music, visual arts, drama, and media production — because every student has a creative voice.")

    # ── Safety Section ────────────────────────
    safety_eyebrow    = models.CharField(max_length=100, default="Your Child's Safety First")
    safety_heading    = models.CharField(max_length=300, default="Health, Safety & Welfare")
    safety_description = models.TextField(
        default="A comprehensive safety ecosystem ensures every student feels secure, cared for, and supported throughout the school day.")

    # ── Gallery Section ───────────────────────
    gallery_subtitle = models.CharField(max_length=100, default="Campus Life")
    gallery_heading  = models.CharField(max_length=300, default="A Glimpse of Azeem School")

    # ── CTA Section ───────────────────────────
    cta_heading       = models.CharField(max_length=200, default="Come See It for Yourself")
    cta_text          = models.TextField(
        default="Nothing describes Azeem School's facilities better than a live campus tour. Book a visit and let your child experience the environment firsthand.")
    cta_btn_label     = models.CharField(max_length=100, default="Book a Campus Tour")
    cta_btn_url       = models.CharField(max_length=255, default="/contact/")
    cta_outline_label = models.CharField(max_length=100, default="Apply Now")
    cta_outline_url   = models.CharField(max_length=255, default="/admissions/")

    # ── Footer ────────────────────────────────
    footer_logo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="facilities_footer_logo",
    )
    footer_newsletter_heading = models.CharField(max_length=200, default="Stay Connected with Azeem School")
    footer_about_title        = models.CharField(max_length=100, default="About Azeem School")
    footer_about_text         = models.TextField(
        default="Azeem School is committed to academic excellence, character development, and world-class facilities that prepare students for a bright future.")
    footer_links_title        = models.CharField(max_length=100, default="Quick Links")
    footer_explore_title      = models.CharField(max_length=100, default="Explore")
    footer_contact_title      = models.CharField(max_length=100, default="Contact Us")
    footer_contact_phone      = models.CharField(max_length=30, default="+92 21 3456 7890")
    footer_contact_email      = models.EmailField(default="info@azeem.edu.pk")
    footer_contact_address    = models.CharField(max_length=300, default="Main Campus, Azeem Road, Karachi")
    footer_contact_map_url    = models.URLField(blank=True)
    footer_copyright_text     = models.CharField(max_length=200, default="© 2025 Azeem School. All Rights Reserved.")

    # ──────────────────────────────────────────
    # ADMIN PANELS
    # ──────────────────────────────────────────

    content_panels = Page.content_panels + [

        MultiFieldPanel([
            FieldPanel("banner_bg_image"),
            FieldPanel("banner_title"),
            FieldPanel("banner_description"),
        ], heading="Sub-Banner"),

        MultiFieldPanel([
            InlinePanel("facility_stats", label="Stat Items (show 4)"),
        ], heading="Stats Strip"),

        MultiFieldPanel([
            FieldPanel("overview_subtitle"),
            FieldPanel("overview_heading"),
            FieldPanel("overview_description"),
            InlinePanel("overview_tiles", label="Overview Tiles (icon grid — show 8)"),
        ], heading="Facilities Overview"),

        MultiFieldPanel([
            FieldPanel("labs_subtitle"),
            FieldPanel("labs_heading"),
            FieldPanel("labs_description"),
            InlinePanel("facility_labs", label="Laboratory Cards"),
        ], heading="Academic Laboratories"),

        MultiFieldPanel([
            FieldPanel("sports_subtitle"),
            FieldPanel("sports_heading"),
            FieldPanel("sports_description"),
            InlinePanel("facility_sports", label="Sports Facility Cards"),
        ], heading="Sports & Athletics"),

        MultiFieldPanel([
            FieldPanel("library_subtitle"),
            FieldPanel("library_heading"),
            FieldPanel("library_description"),
            InlinePanel("library_features", label="Library Feature Rows (left column)"),
            FieldRowPanel([FieldPanel("library_panel_eyebrow"), FieldPanel("library_panel_heading")]),
            InlinePanel("library_stats", label="Library Stats (right panel)"),
        ], heading="Library & Resource Centre"),

        MultiFieldPanel([
            FieldPanel("arts_subtitle"),
            FieldPanel("arts_heading"),
            FieldPanel("arts_description"),
            InlinePanel("arts_cards", label="Arts & Performing Arts Cards"),
        ], heading="Arts & Performing Arts"),

        MultiFieldPanel([
            FieldPanel("safety_eyebrow"),
            FieldPanel("safety_heading"),
            FieldPanel("safety_description"),
            InlinePanel("safety_stats", label="Safety Stats Strip (4 numbers)"),
            InlinePanel("safety_cards", label="Safety Feature Cards (6 total — 3 left, 3 right)"),
        ], heading="Health, Safety & Welfare"),

        MultiFieldPanel([
            FieldPanel("cta_heading"),
            FieldPanel("cta_text"),
            FieldRowPanel([FieldPanel("cta_btn_label"), FieldPanel("cta_btn_url")]),
            FieldRowPanel([FieldPanel("cta_outline_label"), FieldPanel("cta_outline_url")]),
        ], heading="CTA Section"),
    ]

    class Meta:
        verbose_name = "Facilities Page"


# ══════════════════════════════════════════════════════════════════
# NEWS & GALLERY PAGE — CHOICE TUPLES
# ══════════════════════════════════════════════════════════════════

NEWS_CATEGORY_CHOICES = [
    # Events & Celebrations
    ("flagship",     "Flagship Event of the Year"),
    ("annual_day",   "Annual Day & Prize Distribution"),
    ("sports_day",   "Sports Day"),
    ("science_fair", "Science Fair & Exhibition"),
    ("cultural",     "Cultural Festival"),
    ("graduation",   "Graduation Ceremony"),
    ("trip",         "Educational Trip & Excursion"),
    # Academics & Exams
    ("result",       "Board Results & Achievements"),
    ("exam_notice",  "Exam Schedule & Notice"),
    ("academic",     "Academic Update"),
    ("award",        "Award & Recognition"),
    ("olympiad",     "Olympiad & Competition"),
    ("cambridge",    "Cambridge / O-A Level"),
    # Sports & Co-curriculars
    ("sports",       "Sports & Athletics"),
    ("inter_school", "Inter-School Tournament"),
    ("arts",         "Arts, Music & Drama"),
    ("debate",       "Debate & Public Speaking"),
    # School Life & Welfare
    ("admissions",   "Admissions Open"),
    ("notice",       "Important Notice"),
    ("welfare",      "Student Welfare & Health"),
    ("community",    "Community & Social Work"),
    ("pakistan_day", "Pakistan Day / National Event"),
    ("ramadan",      "Ramadan & Islamic Events"),
    ("staff",        "Staff & Faculty News"),
]

NEWS_ANN_TYPE_CHOICES = [
    ("academic", "Academic"),
    ("event",    "Event"),
    ("sports",   "Sports"),
    ("exam",     "Exam"),
    ("notice",   "Notice"),
]

NEWS_ANN_ICON_CHOICES = [
    ("fa-solid fa-bell",             "Bell"),
    ("fa-solid fa-thumbtack",        "Pin / Thumbtack"),
    ("fa-solid fa-file-pen",         "File / Exam"),
    ("fa-solid fa-door-open",        "Admissions / Door"),
    ("fa-solid fa-trophy",           "Trophy / Achievement"),
    ("fa-solid fa-chalkboard-user",  "Parent-Teacher Meeting"),
    ("fa-solid fa-flask",            "Science / Lab"),
    ("fa-solid fa-futbol",           "Sports / Football"),
    ("fa-solid fa-bus",              "Transport / Bus"),
    ("fa-solid fa-calendar-days",    "Calendar / Schedule"),
    ("fa-solid fa-graduation-cap",   "Graduation / Results"),
    ("fa-solid fa-star",             "Achievement / Star"),
    ("fa-solid fa-bullhorn",         "Notice / Announcement"),
    ("fa-solid fa-book-open",        "Academics / Books"),
    ("fa-solid fa-music",            "Arts / Music"),
    ("fa-solid fa-heart-pulse",      "Health / Medical"),
    ("fa-solid fa-shield-halved",    "Safety / Security"),
    ("fa-solid fa-utensils",         "Cafeteria"),
    ("fa-solid fa-mosque",           "Prayer / Event"),
    ("fa-solid fa-award",            "Award / Recognition"),
]

NEWS_ANN_ICON_STYLE_CHOICES = [
    ("ai-purple", "Purple"),
    ("ai-lime",   "Lime / Accent"),
    ("ai-blue",   "Blue"),
    ("ai-pink",   "Pink"),
    ("ai-orange", "Orange"),
    ("ai-teal",   "Teal"),
]

NEWS_ANN_BADGE_CHOICES = [
    ("ab-event",    "Event (purple)"),
    ("ab-academic", "Academic (blue)"),
    ("ab-sports",   "Sports (lime)"),
    ("ab-exam",     "Exam (orange)"),
    ("ab-notice",   "Notice (pink)"),
]

NEWS_EVENT_BADGE_CHOICES = [
    ("upcoming", "Upcoming"),
    ("today",    "Today / This Month"),
]

GALLERY_CATEGORY_CHOICES = [
    ("events",    "Events"),
    ("sports",    "Sports"),
    ("arts",      "Arts"),
    ("campus",    "Campus"),
    ("academics", "Academics"),
]


# ══════════════════════════════════════════════════════════════════
# NEWS & GALLERY PAGE — INLINE MODELS
# ══════════════════════════════════════════════════════════════════

class NewsArticle(Orderable):
    page        = ParentalKey("NewsPage", on_delete=models.CASCADE, related_name="news_articles")
    is_featured = models.BooleanField(
        default=False,
        help_text="Mark ONE article as Featured — it shows as the large hero card at the top.",
    )
    image       = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="news_article_image",
        help_text="Article cover photo (recommended: 900 × 600 px)",
    )
    category    = models.CharField(max_length=20, choices=NEWS_CATEGORY_CHOICES, default="event")
    date        = models.DateField(help_text="Publication date shown on the card and in the popup")
    title       = models.CharField(max_length=300)
    excerpt     = models.TextField(
        help_text="Short summary shown on the card (2-3 sentences). Keep it punchy.",
    )
    body        = models.TextField(
        help_text=(
            "Full article body shown inside the popup modal.\n"
            "Use blank lines to separate paragraphs."
        ),
    )
    is_apply_now = models.BooleanField(
        default=False,
        verbose_name='Show "Apply Now" button',
        help_text='If ticked, the card shows an "Apply Now" button linking to /admissions/ instead of "Read More".',
    )

    panels = [
        FieldRowPanel([FieldPanel("is_featured"), FieldPanel("is_apply_now")]),
        FieldPanel("image"),
        FieldRowPanel([FieldPanel("category"), FieldPanel("date")]),
        FieldPanel("title"),
        FieldPanel("excerpt"),
        FieldPanel("body"),
    ]

    _CATEGORY_CSS_MAP = {
        "flagship":     "cat-event",
        "annual_day":   "cat-event",
        "sports_day":   "cat-sports",
        "science_fair": "cat-science",
        "cultural":     "cat-arts",
        "graduation":   "cat-event",
        "trip":         "cat-academic",
        "result":       "cat-academic",
        "exam_notice":  "cat-notice",
        "academic":     "cat-academic",
        "award":        "cat-academic",
        "olympiad":     "cat-science",
        "cambridge":    "cat-academic",
        "sports":       "cat-sports",
        "inter_school": "cat-sports",
        "arts":         "cat-arts",
        "debate":       "cat-arts",
        "admissions":   "cat-notice",
        "notice":       "cat-notice",
        "welfare":      "cat-academic",
        "community":    "cat-event",
        "pakistan_day": "cat-event",
        "ramadan":      "cat-event",
        "staff":        "cat-academic",
    }

    @property
    def category_css(self):
        return self._CATEGORY_CSS_MAP.get(self.category, "cat-event")

    @property
    def category_label(self):
        return dict(NEWS_CATEGORY_CHOICES).get(self.category, self.category.replace("_", " ").title())

    def __str__(self):
        return self.title


class NewsAnnouncement(Orderable):
    page        = ParentalKey("NewsPage", on_delete=models.CASCADE, related_name="news_announcements")
    ann_type    = models.CharField(max_length=20, choices=NEWS_ANN_TYPE_CHOICES, default="notice")
    icon_choice = models.CharField(max_length=100, choices=NEWS_ANN_ICON_CHOICES, default="fa-solid fa-bell")
    icon_style  = models.CharField(max_length=20, choices=NEWS_ANN_ICON_STYLE_CHOICES, default="ai-purple",
                                   help_text="Background colour of the icon box")
    badge_style = models.CharField(max_length=20, choices=NEWS_ANN_BADGE_CHOICES, default="ab-notice",
                                   help_text="Colour of the category badge pill")
    date_label  = models.CharField(max_length=60,
                                   help_text='Right-side date label, e.g. "May 12, 2025" or "Open till Jul 31"')
    is_pinned   = models.BooleanField(default=False,
                                      help_text="Show a thumbtack pin icon for important / top announcements")
    title       = models.CharField(max_length=300)
    description = models.TextField(help_text="Short description shown below the title")

    panels = [
        FieldRowPanel([FieldPanel("is_pinned"), FieldPanel("ann_type")]),
        FieldRowPanel([FieldPanel("icon_choice"), FieldPanel("icon_style")]),
        FieldRowPanel([FieldPanel("badge_style"), FieldPanel("date_label")]),
        FieldPanel("title"),
        FieldPanel("description"),
    ]

    def __str__(self):
        return self.title


class NewsUpcomingEvent(Orderable):
    page       = ParentalKey("NewsPage", on_delete=models.CASCADE, related_name="news_upcoming_events")
    day        = models.CharField(max_length=5, help_text='Day number shown in the date box, e.g. "12"')
    month      = models.CharField(max_length=10, help_text='Month abbreviation, e.g. "May" or "Jun"')
    badge_type = models.CharField(max_length=20, choices=NEWS_EVENT_BADGE_CHOICES, default="upcoming")
    title      = models.CharField(max_length=200)
    time       = models.CharField(max_length=60, help_text='e.g. "8:00 AM" or "9:00 AM – 1 PM"')
    location   = models.CharField(max_length=120, help_text='e.g. "Main Hall" or "Sports Ground"')

    panels = [
        FieldRowPanel([FieldPanel("day"), FieldPanel("month"), FieldPanel("badge_type")]),
        FieldPanel("title"),
        FieldRowPanel([FieldPanel("time"), FieldPanel("location")]),
    ]

    def __str__(self):
        return self.title


class NewsGalleryPhoto(Orderable):
    page     = ParentalKey("NewsPage", on_delete=models.CASCADE, related_name="news_gallery_photos")
    image    = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="news_gallery_photo_image",
        help_text="Gallery photo (any aspect ratio — CSS handles the masonry layout)",
    )
    category = models.CharField(max_length=20, choices=GALLERY_CATEGORY_CHOICES, default="events")
    title    = models.CharField(max_length=200, help_text="Shown in the hover overlay")
    alt_text = models.CharField(max_length=200, blank=True, default="",
                                help_text="Accessibility alt text (leave blank to use title)")

    panels = [
        FieldPanel("image"),
        FieldRowPanel([FieldPanel("category"), FieldPanel("title")]),
        FieldPanel("alt_text"),
    ]

    def __str__(self):
        return self.title


# ══════════════════════════════════════════════════════════════════
# NEWS & GALLERY PAGE
# ══════════════════════════════════════════════════════════════════

class NewsPage(Page):

    # ── Banner ────────────────────────────────
    banner_title       = models.CharField(max_length=200, default="News & Gallery")
    banner_description = models.TextField(
        default="Stay updated with the latest happenings, achievements, and moments from across Azeem School.")

    # ── Ticker ────────────────────────────────
    ticker_items = models.TextField(
        default=(
            "Admissions Open for 2025–26 Academic Year — Apply Before July 31st!\n"
            "Annual Sports Day — Friday, 6th June 2025 at Main Ground\n"
            "Grade 10 & 12 Board Exams Begin — 12th May 2025. Best of luck to all students!\n"
            "Science Fair 2025 — Project Submissions Close 20th May. Register Now.\n"
            "Parent-Teacher Meeting — Saturday 24th May, 9 AM to 1 PM"
        ),
        help_text="One announcement per line. These scroll in the lime ticker bar at the top of the page.",
    )

    # ── News Section ──────────────────────────
    news_eyebrow = models.CharField(max_length=100, default="Editor's Pick")
    news_heading = models.CharField(max_length=200, default="Latest from Azeem School")

    # ── Announcements Section ─────────────────
    ann_eyebrow         = models.CharField(max_length=100, default="Notice Board")
    ann_heading         = models.CharField(max_length=200, default="Announcements & Upcoming Events")
    events_panel_heading = models.CharField(max_length=100, default="Upcoming Events")

    # ── Gallery Section ───────────────────────
    gallery_eyebrow     = models.CharField(max_length=100, default="Campus Moments")
    gallery_heading     = models.CharField(max_length=200, default="School Gallery")
    gallery_description = models.TextField(
        default="A visual celebration of life at Azeem School — from classrooms to cricket grounds and everything in between.")

    # ── Newsletter CTA ────────────────────────
    cta_heading = models.CharField(max_length=200, default="Never Miss an Update")
    cta_text    = models.TextField(
        default="Subscribe to the Azeem School newsletter and get announcements, event reminders, and highlights delivered straight to your inbox.")

    # ──────────────────────────────────────────
    # HELPERS
    # ──────────────────────────────────────────

    @property
    def ticker_items_list(self):
        return [t.strip() for t in self.ticker_items.splitlines() if t.strip()]

    @property
    def featured_article(self):
        return self.news_articles.filter(is_featured=True).first()

    # ──────────────────────────────────────────
    # ADMIN PANELS
    # ──────────────────────────────────────────

    content_panels = Page.content_panels + [

        MultiFieldPanel([
            FieldPanel("banner_title"),
            FieldPanel("banner_description"),
        ], heading="Banner"),

        MultiFieldPanel([
            FieldPanel("ticker_items"),
        ], heading="Announcements Ticker (scrolling bar — one item per line)"),

        MultiFieldPanel([
            FieldPanel("news_eyebrow"),
            FieldPanel("news_heading"),
            InlinePanel("news_articles", label="News Articles (mark one as Featured)"),
        ], heading="News Articles"),

        MultiFieldPanel([
            FieldPanel("ann_eyebrow"),
            FieldPanel("ann_heading"),
            InlinePanel("news_announcements", label="Announcements"),
        ], heading="Announcements Board"),

        MultiFieldPanel([
            FieldPanel("events_panel_heading"),
            InlinePanel("news_upcoming_events", label="Upcoming Events"),
        ], heading="Upcoming Events Panel"),

        MultiFieldPanel([
            FieldPanel("gallery_eyebrow"),
            FieldPanel("gallery_heading"),
            FieldPanel("gallery_description"),
            InlinePanel("news_gallery_photos", label="Gallery Photos"),
        ], heading="Gallery"),

        MultiFieldPanel([
            FieldPanel("cta_heading"),
            FieldPanel("cta_text"),
        ], heading="Newsletter CTA"),
    ]

    class Meta:
        verbose_name = "News & Gallery Page"
