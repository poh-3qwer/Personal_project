from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='auth.User')
def save_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
    else:
        if hasattr(instance, 'account'):
            instance.account.save()

class Account(models.Model):

    MODERATOR = 'moderator'
    USER = 'user'
    ADMIN = 'admin'

    ROLE_CHOICES = [(MODERATOR, 'moderator'),
                    (USER, 'user'),
                    (ADMIN, 'admin')
                    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    date_of_registration = models.DateField(auto_now_add=True)
    bio = models.TextField(blank=True, null=True)
    human_name = models.CharField(max_length=30, blank=True, null=True)
    human_surname = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} role:{self.role}'

    def _sync_role_from_user(self):
        if self.user_id:
            if self.user.is_superuser:
                self.role = self.ADMIN
            elif self.user.is_staff:
                self.role = self.MODERATOR
            else:
                self.role = self.USER

    def save(self, *args, **kwargs):
        self._sync_role_from_user()
        super().save(*args, **kwargs)

    def auto_give_role(self):
        self._sync_role_from_user()
        self.save()