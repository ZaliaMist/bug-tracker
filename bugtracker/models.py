from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class MyUser(AbstractUser):
   display_name = models.CharField(
       max_length=100,
       null=True,
       blank=True
   )


class TicketM(models.Model):
    title = models.CharField(max_length=100)
    time = models.DateTimeField(
        default=timezone.now
    )
    description = models.TextField()
    created_by = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="created_by",
        # default=""
    )

    NEW = "New"
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'
    INVALID = 'Invalid'

    TICKET_STATUS = [
       (NEW, "New"),
       (IN_PROGRESS, 'In Progress'),
       (DONE, 'Done'),
       (INVALID, 'Invalid')
    ]

    choose_stat = models.CharField(
       max_length=11,
       choices=TICKET_STATUS,
       default=NEW
    )

    user_assigned_to_ticket = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name="user_assigned_to_ticket"
    )  
    user_completed_ticket = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        related_name="user_completed_ticket"
    )

    def __str__(self):
        return self.title