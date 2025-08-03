from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import Message, Notification,MessageHistory

@receiver(post_save, sender=Message)
def notify_user_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )
            instance.edited = True