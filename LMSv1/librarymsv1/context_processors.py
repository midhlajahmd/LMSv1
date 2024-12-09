from django.contrib.auth.models import Group

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