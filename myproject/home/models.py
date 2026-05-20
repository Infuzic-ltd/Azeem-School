from django.db import models
from wagtail.models import Page, Orderable
from wagtail.admin.panels import (
    FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
)
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


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


# ──────────────────────────────────────────────
# TRUST SECTION
# ──────────────────────────────────────────────

class TrustCard(Orderable):
    page = ParentalKey("HomePage", on_delete=models.CASCADE, related_name="trust_cards")
    logo = models.ForeignKey(
        "wagtailimages.Image", null=True,
        on_delete=models.SET_NULL, related_name="trust_card_logo",
    )
    heading = models.CharField(max_length=200)
    description = models.TextField()
    url = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("logo"),
        FieldPanel("heading"),
        FieldPanel("description"),
        FieldPanel("url"),
    ]

    def __str__(self):
        return self.heading


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


class AdmissionProgram(Orderable):
    page = ParentalKey("AdmissionsPage", on_delete=models.CASCADE, related_name="admission_programs")
    name = models.CharField(max_length=200, help_text="Program name shown in the dropdown")

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
            InlinePanel("admission_programs", label="Program Dropdown Options"),
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

    # ── Courses ───────────────────────────────
    courses_subtitle = models.CharField(max_length=100, default="")
    courses_title = models.CharField(max_length=300, default="")

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

        MultiFieldPanel([
            FieldPanel("nav_logo"),
            FieldPanel("nav_phone"),
            InlinePanel("navbar_menus", label="Menu Items (with Dropdowns)"),
            FieldRowPanel([FieldPanel("nav_btn_label"), FieldPanel("nav_btn_url")]),
        ], heading="Navbar"),

        MultiFieldPanel([
            FieldPanel("hero_bg_image"),
            FieldPanel("hero_logo"),
            FieldPanel("hero_headline"),
            FieldPanel("hero_headline_2"),
            FieldPanel("hero_tagline"),
            FieldRowPanel([FieldPanel("hero_btn_label"), FieldPanel("hero_btn_url")]),
        ], heading="Hero"),

        MultiFieldPanel([
            FieldPanel("trust_heading"),
            FieldPanel("trust_description"),
            FieldRowPanel([FieldPanel("trust_btn_label"), FieldPanel("trust_btn_url")]),
            InlinePanel("trust_cards", label="Trust Cards"),
        ], heading="Trust"),

        MultiFieldPanel([
            FieldPanel("about_subtitle"),
            FieldPanel("about_title"),
            FieldPanel("about_description"),
            FieldPanel("about_image_main"),
            FieldPanel("about_image_video_thumb"),
            FieldPanel("about_video_url"),
            FieldPanel("about_mission_icon"),
            FieldPanel("about_mission_title"),
            InlinePanel("about_features", label="Bullet Points"),
        ], heading="About"),

        MultiFieldPanel([
            FieldPanel("courses_subtitle"),
            FieldPanel("courses_title"),
            InlinePanel("course_cards", label="Course Cards"),
        ], heading="Courses"),

        MultiFieldPanel([
            FieldPanel("benefits_subtitle"),
            FieldPanel("benefits_title"),
            InlinePanel("benefit_cards", label="Benefit Cards"),
        ], heading="Benefits / Counter Stats"),

        MultiFieldPanel([
            FieldPanel("journey_logo"),
            FieldPanel("journey_subtitle"),
            FieldPanel("journey_title"),
            FieldRowPanel([FieldPanel("journey_btn_label"), FieldPanel("journey_btn_url")]),
        ], heading="Journey CTA"),

        MultiFieldPanel([
            FieldPanel("testimonials_subtitle"),
            FieldPanel("testimonials_title"),
            InlinePanel("testimonials", label="Testimonials"),
        ], heading="Testimonials"),

        MultiFieldPanel([
            FieldPanel("blog_subtitle"),
            FieldPanel("blog_title"),
            InlinePanel("blog_posts", label="Blog Posts"),
        ], heading="Blog / Articles"),

        MultiFieldPanel([
            FieldPanel("footer_logo"),
            FieldPanel("footer_newsletter_heading"),
            FieldPanel("footer_about_title"),
            FieldPanel("footer_about_text"),
            InlinePanel("footer_social_links", label="Social Links"),
            FieldPanel("footer_links_title"),
            InlinePanel("footer_useful_links", label="Useful Links"),
            FieldPanel("footer_explore_title"),
            InlinePanel("footer_explore_links", label="Explore Links"),
            FieldPanel("footer_contact_title"),
            FieldPanel("footer_contact_phone"),
            FieldPanel("footer_contact_email"),
            FieldPanel("footer_contact_address"),
            FieldPanel("footer_contact_map_url"),
            FieldPanel("footer_copyright_text"),
        ], heading="Footer"),
    ]

    class Meta:
        verbose_name = "Home Page"
