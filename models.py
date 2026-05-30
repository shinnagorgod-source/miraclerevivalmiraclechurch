from django.db import models
from django.utils import timezone


class Sermon(models.Model):
    CATEGORY_CHOICES = [
        ('faith', 'Faith'),
        ('prayer', 'Prayer'),
        ('worship', 'Worship'),
        ('evangelism', 'Evangelism'),
        ('family', 'Family'),
        ('healing', 'Healing'),
        ('prophecy', 'Prophecy'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    speaker = models.CharField(max_length=100, default='Pastor')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True)
    scripture_reference = models.CharField(max_length=100, blank=True)
    # Video: upload a file OR paste a YouTube/Facebook URL
    video_file = models.FileField(
        upload_to='sermons/videos/',
        blank=True, null=True,
        help_text='Upload a video file (MP4 recommended). If both video file and YouTube URL are set, the uploaded file takes priority.'
    )
    youtube_url = models.URLField(
        blank=True,
        help_text='Paste a YouTube or Facebook Watch URL (e.g. https://www.youtube.com/watch?v=...)'
    )
    audio_file = models.FileField(upload_to='sermons/audio/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='sermons/thumbnails/', blank=True, null=True)
    date_preached = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        ordering = ['-date_preached']

    def __str__(self):
        return self.title

    def get_youtube_embed(self):
        if not self.youtube_url:
            return ''
        url = self.youtube_url
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
        elif 'v=' in url:
            video_id = url.split('v=')[-1].split('&')[0]
        else:
            return url
        return f'https://www.youtube.com/embed/{video_id}?rel=0'

    def has_video(self):
        return bool(self.video_file or self.youtube_url)


class Announcement(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High — Urgent'),
    ]
    title = models.CharField(max_length=200)
    body = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True, help_text='Leave blank to show indefinitely')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.title


class Testimony(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=200, help_text='Short title for the testimony')
    testimony = models.TextField()
    photo = models.ImageField(upload_to='testimonies/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = 'Testimonies'

    def __str__(self):
        return f'{self.name} — {self.title}'


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, default='Miracle Church Revival Fellowship')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    # Events can also have a livestream/video link
    livestream_url = models.URLField(blank=True, help_text='YouTube/Facebook livestream link for this event')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    def is_upcoming(self):
        return self.start_date >= timezone.now()


class Ministry(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    leader = models.CharField(max_length=100, blank=True)
    schedule = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='ministries/', blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Font Awesome icon name, e.g. fa-music')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Ministries'

    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='staff/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    facebook_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Staff / Leadership'

    def __str__(self):
        return f'{self.name} — {self.title}'


class GalleryPhoto(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f'{self.name} — {self.subject}'


class PrayerRequest(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    prayer_request = models.TextField()
    is_private = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)
    pastoral_notes = models.TextField(blank=True, help_text='Internal notes for pastoral team only')

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Prayer Request'
        verbose_name_plural = 'Prayer Requests'

    def __str__(self):
        return f'Prayer request from {self.name}'


class ServiceSchedule(models.Model):
    DAY_CHOICES = [
        ('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
        ('Friday', 'Friday'), ('Saturday', 'Saturday'),
    ]
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    service_name = models.CharField(max_length=100)
    time = models.TimeField()
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Service Schedule'
        verbose_name_plural = 'Service Schedules'

    def __str__(self):
        return f'{self.day} — {self.service_name}'


class QuizQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('normal', 'Normal'),
        ('hard', 'Hard'),
        ('expert', 'Expert'),
    ]
    ANSWER_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]

    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    question = models.TextField()
    choice_a = models.CharField(max_length=300)
    choice_b = models.CharField(max_length=300)
    choice_c = models.CharField(max_length=300)
    choice_d = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    explanation = models.TextField(blank=True, help_text='Brief explanation shown after answering')
    scripture_reference = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['difficulty', 'order']
        verbose_name = 'Quiz Question'
        verbose_name_plural = 'Quiz Questions'

    def __str__(self):
        return f'[{self.get_difficulty_display()}] {self.question[:60]}'


class ChurchVideo(models.Model):
    CATEGORY_CHOICES = [
        ('worship', 'Worship'),
        ('sermon', 'Sermon'),
        ('event', 'Event'),
        ('testimony', 'Testimony'),
        ('outreach', 'Outreach'),
        ('youth', 'Youth'),
        ('other', 'Other'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    video_file = models.FileField(
        upload_to='videos/',
        blank=True, null=True,
        help_text='Upload an MP4 video file. If both file and URL are set, the uploaded file takes priority.'
    )
    youtube_url = models.URLField(
        blank=True,
        help_text='Paste a YouTube or Facebook video/reel URL'
    )
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_featured', 'order', '-uploaded_at']
        verbose_name = 'Church Video'
        verbose_name_plural = 'Church Videos'

    def __str__(self):
        return self.title

    def get_embed_url(self):
        if not self.youtube_url:
            return ''
        url = self.youtube_url
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}?rel=0'
        elif 'youtube.com' in url and 'v=' in url:
            video_id = url.split('v=')[-1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}?rel=0'
        elif 'facebook.com' in url:
            import urllib.parse
            encoded = urllib.parse.quote(url, safe='')
            return f'https://www.facebook.com/plugins/video.php?href={encoded}&show_text=false&width=560&autoplay=false'
        return url

    def get_youtube_embed(self):
        return self.get_embed_url()

    def is_facebook(self):
        return bool(self.youtube_url and 'facebook.com' in self.youtube_url)

    def has_video(self):
        return bool(self.video_file or self.youtube_url)
