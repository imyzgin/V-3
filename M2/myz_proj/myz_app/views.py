from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Profile, Request, Review
from .forms import RegisterForm, RequestForm, ReviewForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            
            Profile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                birth_date=form.cleaned_data['birth_date'],
                phone=form.cleaned_data['phone']
            )
            
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def index(request):
    return render(request, 'index.html')

@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            Request.objects.create(
                user=request.user,
                transport_type=form.cleaned_data['transport_type'],
                start_date=form.cleaned_data['start_date'],
                payment_method=form.cleaned_data['payment_method']
            )
            return redirect('my_requests')
    else:
        form = RequestForm()
    return render(request, 'create_request.html', {'form': form})

@login_required
def my_requests(request):
    requests = Request.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_requests.html', {'requests': requests})

@login_required
def leave_review(request, request_id):
    req = get_object_or_404(Request, id=request_id, user=request.user)
    
    if req.status != 'completed':
        messages.error(request, 'Отзыв можно оставить только после завершения обучения')
        return redirect('my_requests')
    
    if hasattr(req, 'review'):
        messages.error(request, 'Вы уже оставили отзыв на эту заявку')
        return redirect('my_requests')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                user=request.user,
                request=req,
                text=form.cleaned_data['text'],
                rating=int(form.cleaned_data['rating'])
            )
            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('my_requests')
    else:
        form = ReviewForm()
    
    return render(request, 'leave_review.html', {'form': form, 'request_item': req})

@login_required
def admin_panel(request):
    if not request.user.is_staff:
        return redirect('index')
    
    requests_list = Request.objects.all().order_by('-created_at')
    paginator = Paginator(requests_list, 5)  # По 5 заявок на страницу
    
    page_number = request.GET.get('page')
    requests = paginator.get_page(page_number)
    
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('status')
        req = get_object_or_404(Request, id=request_id)
        req.status = new_status
        req.save()
        return redirect('admin_panel')
    
    return render(request, 'admin_panel.html', {'requests': requests})