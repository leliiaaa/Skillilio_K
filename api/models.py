from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)    
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True, default='Україна')
    city = models.CharField(max_length=100, blank=True)
    
    is_freelance = models.BooleanField(default=True, verbose_name="Фріланс-проєкти")
    is_remote = models.BooleanField(default=False, verbose_name="Постійна віддалена робота")

    def __str__(self):
        return f"Profile of {self.user.username}"

class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=200)                
    description = models.TextField()                       
    budget = models.IntegerField()                      
    created_at = models.DateTimeField(auto_now_add=True)       
    
    def __str__(self):
        return self.title

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"
    
    class Meta:
        ordering = ['timestamp']

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

    client = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    budget = models.IntegerField()

    category = models.CharField(max_length=50, choices=CATEGORIES, default='other')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title        