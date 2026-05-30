from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    Sermon, Announcement, Testimony, Event, Ministry,
    Staff, GalleryPhoto, ContactMessage, PrayerRequest, ServiceSchedule, QuizQuestion, ChurchVideo
)

admin.site.site_header = '✝ MRFC Church Admin'
admin.site.site_title = 'MRFC Admin'
admin.site.index_title = 'Miracle Church Revival Fellowship — Dashboard'


# ===== SERMON =====
@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'category', 'date_preached', 'video_preview', 'is_featured', 'views']
    list_filter = ['category', 'is_featured', 'date_preached']
    search_fields = ['title', 'speaker', 'description', 'scripture_reference']
    list_editable = ['is_featured']
    date_hierarchy = 'date_preached'
    readonly_fields = ['views', 'created_at', 'thumbnail_preview', 'video_preview_full']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'speaker', 'category', 'date_preached', 'scripture_reference', 'description')
        }),
        ('Media — Video', {
            'fields': ('video_file', 'video_preview_full', 'youtube_url'),
            'description': 'Upload an MP4 video file OR paste a YouTube URL. Uploaded file takes priority over YouTube URL.',
        }),
        ('Media — Audio & Thumbnail', {
            'fields': ('audio_file', 'thumbnail', 'thumbnail_preview'),
            'classes': ('collapse',),
        }),
        ('Settings', {
            'fields': ('is_featured', 'views', 'created_at'),
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="max-height:120px;border-radius:8px;">', obj.thumbnail.url)
        return '— No thumbnail —'
    thumbnail_preview.short_description = 'Thumbnail Preview'

    def video_preview(self, obj):
        if obj.video_file:
            return format_html('<span style="color:green;font-weight:bold;">📹 Video File</span>')
        elif obj.youtube_url:
            return format_html('<span style="color:#c00;font-weight:bold;">▶ YouTube</span>')
        return format_html('<span style="color:#999;">No video</span>')
    video_preview.short_description = 'Video'

    def video_preview_full(self, obj):
        if obj.video_file:
            return format_html(
                '<video controls style="max-width:400px;border-radius:8px;"><source src="{}"></video>', obj.video_file.url
            )
        elif obj.youtube_url:
            embed = obj.get_youtube_embed()
            if embed:
                return format_html('<iframe width="400" height="225" src="{}" frameborder="0" allowfullscreen style="border-radius:8px;"></iframe>', embed)
        return '— No video set yet —'
    video_preview_full.short_description = 'Video Preview'

    actions = ['mark_featured', 'unmark_featured']

    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} sermon(s) marked as featured.')
    mark_featured.short_description = 'Mark selected as Featured'

    def unmark_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f'{queryset.count()} sermon(s) removed from featured.')
    unmark_featured.short_description = 'Remove from Featured'


# ===== ANNOUNCEMENT =====
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_active', 'start_date', 'end_date']
    list_filter = ['priority', 'is_active']
    list_editable = ['is_active', 'priority']
    search_fields = ['title', 'body']

    fieldsets = (
        ('Announcement', {
            'fields': ('title', 'body', 'priority')
        }),
        ('Visibility', {
            'fields': ('is_active', 'start_date', 'end_date'),
            'description': 'Control when this announcement is shown on the website.'
        }),
    )


# ===== TESTIMONY =====
@admin.register(Testimony)
class TestimonyAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'is_approved', 'is_featured', 'submitted_at', 'photo_preview']
    list_filter = ['is_approved', 'is_featured']
    list_editable = ['is_approved', 'is_featured']
    search_fields = ['name', 'title', 'testimony']
    readonly_fields = ['submitted_at', 'photo_preview']

    fieldsets = (
        ('Testimony Details', {
            'fields': ('name', 'title', 'testimony', 'photo', 'photo_preview')
        }),
        ('Settings', {
            'fields': ('is_approved', 'is_featured', 'submitted_at')
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:80px;height:80px;border-radius:50%;object-fit:cover;">', obj.photo.url)
        return '—'
    photo_preview.short_description = 'Photo'


# ===== EVENT =====
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'location', 'is_featured', 'image_preview', 'is_upcoming_display']
    list_filter = ['is_featured', 'start_date']
    search_fields = ['title', 'description', 'location']
    list_editable = ['is_featured']
    readonly_fields = ['image_preview', 'created_at']

    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'description', 'location')
        }),
        ('Date & Time', {
            'fields': ('start_date', 'end_date')
        }),
        ('Media', {
            'fields': ('image', 'image_preview', 'livestream_url'),
            'description': 'Upload an event banner image and/or add a livestream link.'
        }),
        ('Settings', {
            'fields': ('is_featured', 'created_at')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:80px;border-radius:6px;">', obj.image.url)
        return '—'
    image_preview.short_description = 'Image'

    def is_upcoming_display(self, obj):
        if obj.is_upcoming():
            return format_html('<span style="color:green;font-weight:bold;">✔ Upcoming</span>')
        return format_html('<span style="color:#999;">Past</span>')
    is_upcoming_display.short_description = 'Status'


# ===== MINISTRY =====
@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'schedule', 'order', 'image_preview']
    list_editable = ['order']
    search_fields = ['name', 'description', 'leader']
    readonly_fields = ['image_preview']

    fieldsets = (
        ('Ministry Info', {
            'fields': ('name', 'description', 'leader', 'schedule')
        }),
        ('Display', {
            'fields': ('icon', 'image', 'image_preview', 'order'),
            'description': 'Icon: use Font Awesome class name like fa-music, fa-fire, fa-users, etc.'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:80px;border-radius:6px;">', obj.image.url)
        return '—'
    image_preview.short_description = 'Image'


# ===== STAFF =====
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['photo_preview', 'name', 'title', 'email', 'order']
    list_editable = ['order']
    search_fields = ['name', 'title', 'bio']
    readonly_fields = ['photo_preview']

    fieldsets = (
        ('Personal Info', {
            'fields': ('name', 'title', 'bio')
        }),
        ('Photo', {
            'fields': ('photo', 'photo_preview')
        }),
        ('Contact & Social', {
            'fields': ('email', 'phone', 'facebook_url')
        }),
        ('Order', {
            'fields': ('order',),
            'description': 'Lower number = shown first on the website.'
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:60px;height:60px;border-radius:50%;object-fit:cover;border:2px solid #7B2D8B;">', obj.photo.url)
        return format_html('<div style="width:60px;height:60px;border-radius:50%;background:#7B2D8B;display:flex;align-items:center;justify-content:center;color:white;font-size:1.5rem;">👤</div>')
    photo_preview.short_description = 'Photo'


# ===== GALLERY =====
@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ['image_preview', 'title', 'caption', 'uploaded_at']
    search_fields = ['title', 'caption']
    readonly_fields = ['uploaded_at', 'image_preview']

    fieldsets = (
        ('Photo', {
            'fields': ('image', 'image_preview', 'title', 'caption', 'uploaded_at')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:100px;max-width:150px;border-radius:6px;object-fit:cover;">', obj.image.url)
        return '—'
    image_preview.short_description = 'Preview'


# ===== CONTACT MESSAGES =====
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'submitted_at', 'is_read']
    list_filter = ['is_read', 'submitted_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'submitted_at']
    list_editable = ['is_read']

    fieldsets = (
        ('Sender', {'fields': ('name', 'email', 'phone', 'submitted_at')}),
        ('Message', {'fields': ('subject', 'message')}),
        ('Status', {'fields': ('is_read',)}),
    )

    actions = ['mark_read', 'mark_unread']

    def mark_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_read.short_description = 'Mark selected as Read'

    def mark_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_unread.short_description = 'Mark selected as Unread'


# ===== PRAYER REQUESTS =====
@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_private', 'is_answered', 'submitted_at']
    list_filter = ['is_private', 'is_answered', 'submitted_at']
    list_editable = ['is_answered']
    search_fields = ['name', 'email', 'prayer_request']
    readonly_fields = ['name', 'email', 'prayer_request', 'is_private', 'submitted_at']

    fieldsets = (
        ('Requester', {'fields': ('name', 'email', 'submitted_at', 'is_private')}),
        ('Prayer Request', {'fields': ('prayer_request',)}),
        ('Pastoral', {'fields': ('is_answered', 'pastoral_notes')}),
    )


# ===== SERVICE SCHEDULE =====
@admin.register(ServiceSchedule)
class ServiceScheduleAdmin(admin.ModelAdmin):
    list_display = ['day', 'service_name', 'time', 'description', 'order']
    list_editable = ['order', 'time']
    ordering = ['order']


# ===== BIBLE QUIZ =====
@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_short', 'difficulty', 'correct_answer', 'scripture_reference', 'is_active', 'order']
    list_filter = ['difficulty', 'is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['question', 'explanation', 'scripture_reference']
    ordering = ['difficulty', 'order']

    fieldsets = (
        ('Question', {
            'fields': ('difficulty', 'question', 'is_active', 'order')
        }),
        ('Answer Choices', {
            'fields': ('choice_a', 'choice_b', 'choice_c', 'choice_d', 'correct_answer'),
            'description': 'Enter four choices (A, B, C, D) and select which one is correct.'
        }),
        ('Reference & Explanation', {
            'fields': ('scripture_reference', 'explanation'),
            'description': 'The explanation is shown to the player after they answer.'
        }),
    )

    def question_short(self, obj):
        return obj.question[:70] + '...' if len(obj.question) > 70 else obj.question
    question_short.short_description = 'Question'


# ===== CHURCH VIDEOS =====
@admin.register(ChurchVideo)
class ChurchVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'video_source', 'thumbnail_preview', 'is_featured', 'is_active', 'order', 'uploaded_at']
    list_filter = ['category', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active', 'order']
    search_fields = ['title', 'description']
    readonly_fields = ['uploaded_at', 'thumbnail_preview', 'video_preview']

    fieldsets = (
        ('Video Info', {
            'fields': ('title', 'description', 'category', 'is_featured', 'is_active', 'order')
        }),
        ('Video Source', {
            'fields': ('video_file', 'youtube_url', 'video_preview'),
            'description': 'Upload an MP4 file OR paste a YouTube URL. Uploaded file takes priority.'
        }),
        ('Thumbnail', {
            'fields': ('thumbnail', 'thumbnail_preview'),
            'description': 'Optional cover image shown before the video plays.'
        }),
        ('Info', {
            'fields': ('uploaded_at',)
        }),
    )

    def video_source(self, obj):
        if obj.video_file:
            return format_html('<span style="color:green;font-weight:bold;">📹 Uploaded File</span>')
        elif obj.youtube_url:
            return format_html('<span style="color:#c00;font-weight:bold;">▶ YouTube</span>')
        return format_html('<span style="color:#999;">No video</span>')
    video_source.short_description = 'Source'

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="max-height:80px;border-radius:6px;">', obj.thumbnail.url)
        return '—'
    thumbnail_preview.short_description = 'Thumbnail'

    def video_preview(self, obj):
        if obj.video_file:
            return format_html(
                '<video controls style="max-width:400px;border-radius:8px;"><source src="{}"></video>', obj.video_file.url
            )
        elif obj.youtube_url:
            embed = obj.get_youtube_embed()
            if embed:
                return format_html(
                    '<iframe width="400" height="225" src="{}" frameborder="0" allowfullscreen style="border-radius:8px;"></iframe>', embed
                )
        return '— No video set yet —'
    video_preview.short_description = 'Preview'
