from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from unidecode import unidecode
from django.template import defaultfilters


from .models import Action, User
from .forms import RegistrationForm, LoginForm, AddActionForm


def choose_template(template):
    def render_todos(func):
        def wraps(*args, **kwargs):

            result = func(*args, **kwargs)
            print(result)

            if isinstance(result, tuple):
                context = {
                        'objs': result[0],
                        'is_archived': result[1],
                    }
            else:
                context = {
                    'objs': result,
                }

            return render(
                args[0],
                template,
                context,
            )

        return wraps

    return render_todos


@choose_template('todo/actions.html')
def index(request):

    return Action.objects.filter(status='опубликовано').all(), False


@choose_template('todo/actions.html')
def todo_archived(request):

    return Action.objects.filter(status='неопубликовано').all(), True


@choose_template('todo/action.html')
def todo(request, slug):

    return Action.objects.filter(slug=slug).get()


def register_user(request):
    if request.method == 'POST':

        registration_form = RegistrationForm(request.POST)

        if request.POST['password1'] != request.POST['password2']:
            return render(
                request,
                'todo/register.html',
                {
                    'form': RegistrationForm(),
                    'message': 'Пароли не совпадают!',
                }
            )

        elif registration_form.is_valid():
            try:
                new_user = User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password1']
                )
                new_user.save()
            except IntegrityError:
                return render(
                    request,
                    'todo/register.html',
                    {
                        'form': RegistrationForm(),
                        'message': 'Пользователь с таким именем уже существует!'
                    }
                )

            login(request, new_user)
            return HttpResponseRedirect(reverse('index'))
    else:
        return render(
            request,
            'todo/register.html',
            {
                'form': RegistrationForm(),
            }
        )


def login_user(request):
    if request.method == 'POST':

        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password'],
        )

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(
                request,
                'todo/login.html',
                {
                    'form': LoginForm(),
                    'message': 'Вы ввели неверные данные!',
                }
            )
    else:
        return render(
            request,
            'todo/login.html',
            {
                'form': LoginForm(),
            }
        )


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def create_action(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        new_action = Action.objects.create(
            title=title,
            content=content,
            user=request.user,
            slug=defaultfilters.slugify(unidecode(title)),
        )
        new_action.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(
            request,
            'todo/add_action.html',
            {
                'form': AddActionForm
            }
        )


def to_archive(request, slug):

    to_arch = Action.objects.filter(slug=slug).get()
    to_arch.status = 'неопубликовано'
    to_arch.save()

    return HttpResponseRedirect(reverse('archive'))


def from_archive(request, slug):

    from_arch = Action.objects.filter(slug=slug).get()
    from_arch.status = 'опубликовано'
    from_arch.save()

    return HttpResponseRedirect(reverse('index'))