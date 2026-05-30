from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Sermon, Announcement, Testimony, Event, Ministry, Staff, GalleryPhoto, ServiceSchedule, QuizQuestion, ChurchVideo
from .forms import ContactForm, PrayerRequestForm


def home(request):
    today = timezone.now().date()
    announcements = Announcement.objects.filter(
        is_active=True,
        start_date__lte=today
    ).filter(Q(end_date__isnull=True) | Q(end_date__gte=today))[:5]

    featured_sermons = Sermon.objects.filter(is_featured=True)[:3]
    latest_sermons = Sermon.objects.all()[:3]
    upcoming_events = Event.objects.filter(start_date__gte=timezone.now())[:3]
    ministries = Ministry.objects.all()[:6]
    gallery_photos = GalleryPhoto.objects.all()[:8]
    schedules = ServiceSchedule.objects.all()
    testimonies = Testimony.objects.filter(is_approved=True, is_featured=True)[:3]
    highlight_video = ChurchVideo.objects.filter(is_active=True, is_featured=True).first()

    context = {
        'announcements': announcements,
        'featured_sermons': featured_sermons,
        'latest_sermons': latest_sermons,
        'upcoming_events': upcoming_events,
        'ministries': ministries,
        'gallery_photos': gallery_photos,
        'schedules': schedules,
        'testimonies': testimonies,
        'highlight_video': highlight_video,
    }
    return render(request, 'church/home.html', context)


def about(request):
    staff = Staff.objects.all()
    testimonies = Testimony.objects.filter(is_approved=True)[:6]
    return render(request, 'church/about.html', {'staff': staff, 'testimonies': testimonies})


def sermons(request):
    category = request.GET.get('category', '')
    sermon_list = Sermon.objects.all()
    if category:
        sermon_list = sermon_list.filter(category=category)
    categories = Sermon.CATEGORY_CHOICES
    return render(request, 'church/sermons.html', {
        'sermons': sermon_list,
        'categories': categories,
        'selected_category': category,
    })


def sermon_detail(request, pk):
    sermon = get_object_or_404(Sermon, pk=pk)
    # Increment view count
    Sermon.objects.filter(pk=pk).update(views=sermon.views + 1)
    related = Sermon.objects.filter(category=sermon.category).exclude(pk=pk)[:3]
    return render(request, 'church/sermon_detail.html', {'sermon': sermon, 'related': related})


def events(request):
    upcoming = Event.objects.filter(start_date__gte=timezone.now())
    past = Event.objects.filter(start_date__lt=timezone.now()).order_by('-start_date')[:6]
    return render(request, 'church/events.html', {'upcoming': upcoming, 'past': past})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'church/event_detail.html', {'event': event})


def ministries(request):
    ministry_list = Ministry.objects.all()
    return render(request, 'church/ministries.html', {'ministries': ministry_list})


def gallery(request):
    photos = GalleryPhoto.objects.all()
    return render(request, 'church/gallery.html', {'photos': photos})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent. We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'church/contact.html', {'form': form})


def prayer_request(request):
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your prayer request has been submitted. Our team will be praying for you!')
            return redirect('prayer_request')
    else:
        form = PrayerRequestForm()
    return render(request, 'church/prayer_request.html', {'form': form})


def give(request):
    return render(request, 'church/give.html')


def videos(request):
    category = request.GET.get('category', '')
    video_list = ChurchVideo.objects.filter(is_active=True)
    if category:
        video_list = video_list.filter(category=category)
    categories = ChurchVideo.CATEGORY_CHOICES
    return render(request, 'church/videos.html', {
        'videos': video_list,
        'categories': categories,
        'selected_category': category,
    })


def quiz(request):
    counts = {
        'easy': QuizQuestion.objects.filter(difficulty='easy', is_active=True).count(),
        'normal': QuizQuestion.objects.filter(difficulty='normal', is_active=True).count(),
        'hard': QuizQuestion.objects.filter(difficulty='hard', is_active=True).count(),
        'expert': QuizQuestion.objects.filter(difficulty='expert', is_active=True).count(),
    }
    return render(request, 'church/quiz.html', {'counts': counts})


def quiz_play(request, difficulty):
    valid = ['easy', 'normal', 'hard', 'expert']
    if difficulty not in valid:
        return redirect('quiz')
    questions = list(QuizQuestion.objects.filter(difficulty=difficulty, is_active=True).values(
        'id', 'question', 'choice_a', 'choice_b', 'choice_c', 'choice_d',
        'correct_answer', 'explanation', 'scripture_reference'
    ))
    import json
    return render(request, 'church/quiz_play.html', {
        'difficulty': difficulty,
        'difficulty_display': difficulty.title(),
        'questions_json': json.dumps(questions),
        'question_count': len(questions),
    })
