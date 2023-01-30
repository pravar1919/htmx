from django.db.models import Max
from films.models import UserFilms


def get_max_order(user):
    existing_film = UserFilms.objects.filter(user=user)
    if not existing_film.exists():
        return 1
    else:
        current_max = existing_film.aggregate(max_order=Max("order"))["max_order"]
        return current_max + 1