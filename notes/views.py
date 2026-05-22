import os

from dotenv import load_dotenv

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

from .models import Note

from openai import OpenAI


# LOAD ENV
load_dotenv()


# DEEPSEEK API
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


@login_required(login_url='/login/')
def home(request):

    query = request.GET.get('q')

    notes = Note.objects.filter(
        user=request.user
    )

    if query:

        notes = notes.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(subject__icontains=query)
        )

    notes = notes.order_by('-created_at')

    return render(request, 'index.html', {
        'notes': notes
    })


def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)
            return redirect('/')

        else:
            messages.error(request, 'Username atau password salah')

    return render(request, 'auth/login.html')


def register_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():

            messages.error(request, 'Username sudah digunakan')

        else:

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(request, 'Register berhasil')

            return redirect('/login/')

    return render(request, 'auth/register.html')


def logout_view(request):

    logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def add_note(request):

    if request.method == 'POST':

        subject = request.POST['subject']
        title = request.POST['title']
        content = request.POST['content']

        Note.objects.create(
            user=request.user,
            subject=subject,
            title=title,
            content=content
        )

        return redirect('/')

    return render(request, 'add_note.html')


@login_required(login_url='/login/')
def note_detail(request, id):

    note = get_object_or_404(
        Note,
        id=id,
        user=request.user
    )

    return render(request, 'detail_note.html', {
        'note': note
    })


@login_required(login_url='/login/')
def edit_note(request, id):

    note = get_object_or_404(
        Note,
        id=id,
        user=request.user
    )

    if request.method == 'POST':

        note.subject = request.POST['subject']
        note.title = request.POST['title']
        note.content = request.POST['content']

        note.save()

        return redirect('/')

    return render(request, 'edit_note.html', {
        'note': note
    })


@login_required(login_url='/login/')
def delete_note(request, id):

    note = get_object_or_404(
        Note,
        id=id,
        user=request.user
    )

    note.delete()

    return redirect('/')


@login_required(login_url='/login/')
def generate_summary(request, id):

    note = get_object_or_404(
        Note,
        id=id,
        user=request.user
    )

    try:

        response = client.chat.completions.create(
            model="deepseek-chat",

            messages=[

                {
                    "role": "system",
                    "content": (
                        "Kamu adalah AI pembantu mahasiswa. "
                        "Buat ringkasan materi kuliah yang rapi, "
                        "mudah dipahami menggunakan paragraf biasa. "
                        "Jangan gunakan markdown seperti ##, **, tabel, atau code block."
                    )
                },

                {
                    "role": "user",
                    "content": note.content
                }

            ],

            temperature=0.7,
            max_tokens=500
        )

        result = response.choices[0].message.content

        note.summary = result

        note.save()

    except Exception as e:

        note.summary = f'Terjadi error AI: {str(e)}'

        note.save()

    return redirect(f'/note/{note.id}/')


# API JSON NOTES
@login_required(login_url='/login/')
def api_notes(request):

    notes = Note.objects.filter(
        user=request.user
    ).values(
        'id',
        'title',
        'subject',
        'content'
    )

    return JsonResponse(
        list(notes),
        safe=False
    )