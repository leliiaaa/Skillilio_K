from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Order
from .forms import OrderForm, UserUpdateForm, ProfileUpdateForm
from django.db.models import Q
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404 

def index(request):
    return render(request, 'index.html')

def auth_page(request):
    if request.user.is_authenticated:
        return redirect('check_role')
    return render(request, 'auth.html')

@login_required
def check_role(request):
    if hasattr(request.user, 'profile') and request.user.profile.role:
        return redirect('dashboard')
    else:
        return redirect('select_role')

@login_required
def select_role(request):
    return render(request, 'select_role.html')

@login_required
def save_role(request, role_type):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.role = role_type
    profile.save()
    return redirect('dashboard')

@login_required
def dashboard(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    my_orders = Order.objects.filter(client=request.user).order_by('-created_at')
    
    all_orders = Order.objects.all().order_by('-created_at')

    cat = request.GET.get('cat') 
    
    if cat and cat != 'all':     
        all_orders = all_orders.filter(category=cat)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'my_orders': my_orders, 
        'all_orders': all_orders,
        'active_cat': cat 
    }
    return render(request, 'dashboard.html', context)

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.save()
            return redirect('dashboard')
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})

@login_required
def settings_page(request):
    Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('settings')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'settings.html', context)

@login_required
def inbox(request):
    messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    
    dialog_partners = set()
    for msg in messages:
        if msg.sender == request.user:
            dialog_partners.add(msg.receiver)
        else:
            dialog_partners.add(msg.sender)
            
    return render(request, 'inbox.html', {'dialog_partners': dialog_partners})

@login_required
def chat_room(request, user_id):
    other_user = User.objects.get(id=user_id)
    
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.save()
            return redirect('chat_room', user_id=user_id)
    else:
        form = MessageForm()
        
    return render(request, 'chat_room.html', {
        'other_user': other_user,
        'messages': messages,
        'form': form
    })    

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.client != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = OrderForm(instance=order)
    
    return render(request, 'create_order.html', {'form': form, 'is_edit': True})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def ai_interview_start(request, order_id):
    """
    Ця функція - заготовка для майбутнього ШІ.
    Сюди фрілансер потрапляє після натискання "Хочу це завдання".
    Поки що просто покажемо сторінку-заглушку.
    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'ai_interview.html', {'order': order})