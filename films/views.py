from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from films.models import Film, UserFilms
from django.views.generic.list import ListView

from films.forms import RegisterForm
from films.utils import get_max_order


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    
class Login(LoginView):
    template_name = 'registration/login.html'

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)

class FilmList(ListView):
    template_name = 'films.html'
    model = Film
    context_object_name = 'films'

    def get_queryset(self):
        user = self.request.user
        return UserFilms.objects.filter(user=self.request.user)

def check_username(request):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div style='color:red;'>Username is not Available</div>")
    return HttpResponse("<div style='color:green;'>Username is Available</div>")

def add_film(request):
    name=request.POST.get("filmname")
    film, _ = Film.objects.get_or_create(name=name)

    if not UserFilms.objects.filter(film=film, user=request.user).exists():
        UserFilms.objects.create(
            film=film, 
            user=request.user, 
            order=get_max_order(request.user)
        )

    films = UserFilms.objects.filter(user=request.user)
    return render(request, 'partials/film-list.html', {'films':films})

def delete_film(request, pk):
    UserFilms.objects.get(pk=pk).delete()

    films = UserFilms.objects.filter(user=request.user)
    return render(request, 'partials/film-list.html', {'films':films})


def sort_film(request):
    film_pk_order = request.POST.getlist('film_order')
    films = []
    for idx, film_pk in enumerate(film_pk_order, start=1):
        userfilm = UserFilms.objects.get(pk=film_pk)
        userfilm.order = idx
        userfilm.save()
        films.append(userfilm)

    return render(request, 'partials/film-list.html', {'films':films})