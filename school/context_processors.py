from .models import Grade

def grades_context(request):
    if request.user.is_authenticated and hasattr(request.user, 'school'):
        grades = Grade.objects.filter(school=request.user.school)
        return {'grades': grades}
    return {}