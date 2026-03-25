import asyncio
import edge_tts
import os
import fitz  # PyMuPDF

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import ConvertedFile


async def generate_voice(text, output_path):
    communicate = edge_tts.Communicate(text, "kk-KZ-AigulNeural")
    await communicate.save(output_path)


@login_required
def home(request):
    audio_url = None
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']

        os.makedirs('media/uploads', exist_ok=True)
        os.makedirs('media/audio', exist_ok=True)

        try:
            doc = fitz.open(stream=myfile.read(), filetype="pdf")
            full_text = ""
            for page in doc:
                full_text += page.get_text()

            if full_text.strip():
                audio_name = f"{os.path.splitext(myfile.name)[0]}.mp3"
                audio_path = os.path.join('media/audio', audio_name)

                asyncio.run(generate_voice(full_text, audio_path))

                new_file = ConvertedFile.objects.create(
                    user=request.user,
                    title=myfile.name,
                    original_pdf=myfile,
                    converted_audio=f"audio/{audio_name}"
                )
                audio_url = new_file.converted_audio.url

        except Exception as e:
            print(f"Қате орын алды: {e}")

    return render(request, 'core/index.html', {'audio_url': audio_url})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():          # ← осы жерді түзеттік
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    user_files = ConvertedFile.objects.filter(
        user=request.user
    ).order_by('-created_at')
    return render(request, 'core/profile.html', {'user_files': user_files})


def about(request):
    return render(request, 'core/about.html')


@login_required
def settings_view(request):
    return render(request, 'core/settings.html')