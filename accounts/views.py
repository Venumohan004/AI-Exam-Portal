# Create your views here.
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import StudentRegistrationForm


def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = StudentRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})
