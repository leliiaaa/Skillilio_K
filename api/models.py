from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    role = models.CharField(max_length=20, default='client') # choices
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    country = models.CharField(max_length=100, blank=True, verbose_name="Країна")
    city = models.CharField(max_length=100, blank=True, verbose_name="Місто")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата народження")
    languages = models.CharField(max_length=200, blank=True, verbose_name="Знання мов")
    bio = models.TextField(blank=True, verbose_name="Про себе") 
    
    is_freelance = models.BooleanField(default=False, verbose_name="Шукаю проєкти")
    is_remote = models.BooleanField(default=False, verbose_name="Тільки віддалено")

    def __str__(self):
        return f'{self.user.username} Profile'

class Order(models.Model):
    CATEGORIES = [
        ('web_dev', 'Веб-розробка'),
        ('backend', 'Backend (Python, PHP, Node.js)'),
        ('frontend', 'Frontend (HTML, CSS, JS, React)'),
        ('mobile', 'Мобільна розробка (Android, iOS)'),
        ('gamedev', 'Розробка ігор (Unity, Unreal)'),
        ('design', 'Дизайн (UI/UX, Логотипи, Арт)'),
        ('qa', 'Тестування (QA Manual/Auto)'),
        ('devops', 'DevOps та Системне адміністрування'),
        ('datascience', 'Data Science, AI та Боти'),
        ('marketing', 'Маркетинг, SEO та SMM'),
        ('copywriting', 'Копірайтинг та Переклади'),
        ('video', 'Аудіо та Відеомонтаж'),
        ('other', 'Інше'),
    ]

    STATUS_CHOICES = [
        ('open', 'Відкрито (Пошук)'),
        ('in_progress', 'В роботі'),
        ('completed', 'Виконано')
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_orders') # Додав related_name для зручності
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.IntegerField()
    requirements = models.TextField(default='', verbose_name="Вимоги до кандидата")
    category = models.CharField(max_length=50, choices=CATEGORIES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='open', 
        verbose_name="Статус"
    )
    
    executor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='executed_orders', 
        verbose_name="Виконавець"
    )

    def __str__(self):
        return self.title

class Interview(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.TextField() # питання ШІ
    answers = models.TextField()   # відповіль юзера
    ai_feedback = models.TextField() # вердикт 
    score = models.IntegerField()  # оцінка (0-100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.freelancer.username} - {self.score}/100"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Поповнення'),
        ('withdrawal', 'Виведення'),
        ('payment', 'Оплата послуг'),
        ('income', 'Зарахування'),
        ('bonus', 'Бонус'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.amount}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()