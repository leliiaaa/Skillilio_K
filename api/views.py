import google.generativeai as genai
import sys
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.models import User
from decimal import Decimal 
from django.db import transaction 
from django.contrib import messages 

from .models import Profile, Order, Message, Transaction, Interview
from .forms import OrderForm, MessageForm, UserUpdateForm, ProfileUpdateForm

def index(request):
    return render(request, 'index.html')

def auth_page(request):
    if request.user.is_authenticated:
        return redirect('check_role')
    return render(request, 'auth.html')

def fake_social_login(request, provider):
    username = f"{provider}_user"
    email = f"{provider}@example.com"
    user, created = User.objects.get_or_create(username=username, defaults={
        'email': email,
        'first_name': f"{provider.capitalize()}",
        'last_name': "User"
    })
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('check_role')

@login_required
def check_role(request):
    if hasattr(request.user, 'profile') and request.user.profile.role:
        return redirect('dashboard')
    return redirect('select_role')

@login_required
def select_role(request):
    return render(request, 'select_role.html')

@login_required
def save_role(request, role_type):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    profile.role = role_type
    profile.save()
    return redirect('dashboard')

@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Профіль оновлено!")
            return redirect('/dashboard/?tab=settings')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    my_orders = Order.objects.filter(client=request.user).order_by('-created_at')
    all_orders = Order.objects.all().order_by('-created_at')

    cat = request.GET.get('cat')
    if cat and cat != 'all':
        all_orders = all_orders.filter(category=cat)

    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    
    trans_filter = request.GET.get('trans_type')
    if trans_filter == 'income':
        transactions = transactions.filter(type__in=['deposit', 'income', 'bonus'])
    elif trans_filter == 'expense':
        transactions = transactions.filter(type__in=['withdrawal', 'payment'])

    income_total = sum(t.amount for t in transactions if t.type in ['deposit', 'income', 'bonus'])
    expense_total = sum(t.amount for t in transactions if t.type in ['withdrawal', 'payment'])

    context = {
        'u_form': u_form, 
        'p_form': p_form,
        'my_orders': my_orders, 
        'all_orders': all_orders,
        'active_cat': cat,
        'transactions': transactions,
        'income_total': income_total, 
        'expense_total': expense_total,
        'active_filter': trans_filter
    }
    return render(request, 'dashboard.html', context)

@login_required
def finance_deposit(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount'))
            Transaction.objects.create(user=request.user, amount=amount, type='deposit', description='Поповнення балансу')
            request.user.profile.balance += amount
            request.user.profile.save()
            messages.success(request, f"Зараховано {amount} грн")
        except: pass
    return redirect('/dashboard/?tab=finance')

@login_required
def finance_withdraw(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount'))
            if request.user.profile.balance >= amount:
                Transaction.objects.create(user=request.user, amount=amount, type='withdrawal', description='Виведення коштів')
                request.user.profile.balance -= amount
                request.user.profile.save()
                messages.success(request, f"Виведено {amount} грн")
            else:
                messages.error(request, "Недостатньо коштів")
        except: pass
    return redirect('/dashboard/?tab=finance')

@login_required
def finance_transfer(request):
    if request.method == 'POST':
        try:
            amount = Decimal(request.POST.get('amount'))
            recipient_username = request.POST.get('username')
            
            if amount <= 0 or request.user.profile.balance < amount:
                messages.error(request, "Некоректна сума")
                return redirect('/dashboard/?tab=finance')
            
            recipient = User.objects.get(username=recipient_username)
            if recipient == request.user: return redirect('/dashboard/?tab=finance')

            with transaction.atomic():
                request.user.profile.balance -= amount
                request.user.profile.save()
                Transaction.objects.create(user=request.user, amount=amount, type='payment', description=f'Переказ {recipient.username}')

                recipient_profile, _ = Profile.objects.get_or_create(user=recipient)
                recipient_profile.balance += amount
                recipient_profile.save()
                Transaction.objects.create(user=recipient, amount=amount, type='income', description=f'Переказ від {request.user.username}')
            
            messages.success(request, f"Надіслано {amount} грн користувачу {recipient.username}")
        except: 
            messages.error(request, "Користувача не знайдено")
    return redirect('/dashboard/?tab=finance')

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.save()
            messages.success(request, "Завдання створено!")
            return redirect('dashboard')
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.client != request.user: return redirect('dashboard')
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Завдання оновлено!")
            return redirect('dashboard')
    else:
        form = OrderForm(instance=order)
    return render(request, 'create_order.html', {'form': form, 'is_edit': True})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    interviews = Interview.objects.filter(order=order).order_by('-score')
    
    best_candidate = interviews.first() if interviews.exists() else None

    return render(request, 'order_detail.html', {
        'order': order,
        'interviews': interviews,
        'best_candidate': best_candidate
    })

@login_required
def ai_interview_start(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if Interview.objects.filter(order=order, freelancer=request.user).exists():
        messages.warning(request, "Ви вже проходили цей тест!")
        return redirect('order_detail', order_id=order.id)

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Ти суворий технічний рекрутер.
    Замовлення: "{order.title}".
    Опис: "{order.description}".
    Вимоги до кандидата: "{order.requirements}".
    
    Сформулюй 3 складних технічних запитання українською мовою, щоб перевірити, чи відповідає кандидат цим вимогам.
    Питання мають бути конкретними. Просто пронумерований список.
    """
    
    try:
        response = model.generate_content(prompt)
        questions = response.text
    except:
        questions = "1. Розкажіть про свій досвід.\n2. Чому ви хочете цей проєкт?\n3. Ваші сильні сторони?"

    return render(request, 'ai_interview.html', {'order': order, 'questions': questions})

@login_required
def ai_interview_check(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        questions = request.POST.get('questions_text')
        user_answers = request.POST.get('user_answers')

       # print("--- СПИСОК ДОСТУПНИХ МОДЕЛЕЙ ---")
       # try:
       #     for m in genai.list_models():
       #        if 'generateContent' in m.supported_generation_methods:
       #             print(m.name)
       # except Exception as e:
       #     print(f"!!! ПОМИЛКА ДОСТУПУ: {e}")
       # print("----------------------------------")

       # print("="*30)
       # print(f"PYTHON EXE: {sys.executable}")
       # print(f"GENAI VERSION: {genai.__version__}")
       # print("="*30)

       # print(f"РЕАЛЬНА ВЕРСІЯ БІБЛІОТЕКИ: {genai.__version__}")

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""
        Я кандидат на фріланс-замовлення.
        Питання були такі:
        {questions}

        Мої відповіді:
        {user_answers}

        Твоє завдання: оцінити мої відповіді як професіонал.
        1. Дай коротку оцінку (фідбек) українською мовою (2-3 речення).
        2. В кінці напиши оцінку від 0 до 100 у форматі: "SCORE: 85".
        """
        
        try:
            response = model.generate_content(prompt)
            feedback_text = response.text
            
            import re
            score_match = re.search(r'SCORE:\s*(\d+)', feedback_text)
            score = int(score_match.group(1)) if score_match else 50
            
            feedback_clean = feedback_text.replace(f"SCORE: {score}", "")

            Interview.objects.create(
                order=order,
                freelancer=request.user,
                questions=questions,
                answers=user_answers,
                ai_feedback=feedback_clean,
                score=score
            )

            return render(request, 'interview_result.html', {
                'order': order, 
                'score': score, 
                'feedback': feedback_clean
            })

        except Exception as e:
            messages.error(request, f"Помилка ШІ: {e}")
            return redirect('order_detail', order_id=order.id)
            
    return redirect('dashboard')

@login_required
def settings_page(request):
    return redirect('dashboard')

@login_required
def inbox(request):
    messages_list = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    dialog_partners = set()
    for msg in messages_list:
        if msg.sender == request.user: dialog_partners.add(msg.receiver)
        else: dialog_partners.add(msg.sender)
    return render(request, 'inbox.html', {'dialog_partners': dialog_partners})

@login_required
def chat_room(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages_list = Message.objects.filter(
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
    return render(request, 'chat_room.html', {'other_user': other_user, 'messages': messages_list, 'form': form})