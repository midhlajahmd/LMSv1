from django.contrib.auth.models import Group
from .models import Notification

def user_roles(request):
    if request.user.is_authenticated:
        is_librarian = request.user.groups.filter(name='Librarian').exists()
        is_student = request.user.groups.filter(name='Student').exists()
        return {'is_librarian': is_librarian,
                'is_student': is_student,
                }
    return {'is_librarian':False,
            'is_student': False,
            }

from .models import Notification

def notifications(request):
    """
    Adds unread notifications to the template context.
    """
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False)
        return {"notifications": unread_notifications}
    return {"notifications": []}