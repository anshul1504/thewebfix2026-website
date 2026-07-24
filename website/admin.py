from django.contrib import admin
from .models import (
    BlogPost, Brochure, CareerOpening, Client, ContentPage, FAQ, FounderProfile,
    Inquiry, JobApplication, NavigationItem, NewsletterSubscriber, ProcessStep, Product, Project, Service,
    SiteSettings, SocialLink, Statistic, Technology, Testimonial,
)

admin.site.site_header = "The Webfix Command Centre"
admin.site.site_title = "The Webfix CMS"
admin.site.index_title = "Brand, content and growth operations"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Brand & theme", {"fields": ("name", "logo", "hero_background", "logo_text", "announcement", "accent_color", "background_color", "font_heading", "font_body")}),
        ("Homepage hero", {"fields": ("hero_eyebrow", "hero_title", "hero_subtitle", "primary_cta_text", "primary_cta_url", "secondary_cta_text", "secondary_cta_url")}),
        ("About", {"fields": ("about_eyebrow", "about_title", "about_body")}),
        ("Contact", {"fields": ("contact_title", "contact_body", "email", "phone", "secondary_phone", "whatsapp_url", "address", "office_hours", "map_embed_url")}),
        ("SEO & analytics", {"fields": ("meta_title", "meta_description", "keywords", "canonical_url", "og_image", "analytics_id")}),
        ("Footer", {"fields": ("footer_text",)}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


class OrderedAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(Service)
class ServiceAdmin(OrderedAdmin):
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description", "overview")
    fieldsets = (
        ("Identity", {"fields": ("title", "slug", "number", "eyebrow", "icon", "hero_image", "order", "is_active")}),
        ("Content", {"fields": ("description", "overview", "benefits", "features", "process", "technologies", "tags")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at", "is_published", "featured")
    list_filter = ("category", "is_published", "featured")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Client)
class ClientAdmin(OrderedAdmin):
    list_filter = ("industry",)
    search_fields = ("name", "industry", "result")


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "created_at", "is_contacted")
    list_filter = ("service", "is_contacted", "created_at")
    search_fields = ("name", "email", "company", "message")
    readonly_fields = ("created_at",)



@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "opening", "experience", "current_location", "status", "created_at")
    list_filter = ("status", "opening", "created_at")
    search_fields = ("name", "email", "phone", "portfolio_url", "linkedin_url", "cover_note")
    readonly_fields = ("created_at",)
    list_editable = ("status",)
@admin.register(NewsletterSubscriber)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at", "is_active")
    list_filter = ("is_active", "created_at")


@admin.register(FAQ)
class FAQAdmin(OrderedAdmin):
    list_display = ("question", "category", "order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("question", "answer")


for model in (NavigationItem, Statistic, ProcessStep, Product, Project, Technology, Testimonial, SocialLink, CareerOpening):
    admin.site.register(model, OrderedAdmin)

admin.site.register(ContentPage)
admin.site.register(FounderProfile)
admin.site.register(Brochure)