from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import reverse

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse('dashboard:home')  # Usando o namespace correto

class CustomLogoutView(LogoutView):
    next_page = 'index'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada com sucesso para {username}!')
            login(request, user)
            return redirect('dashboard:home')  # Usando o namespace correto
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def user_settings(request):
    """View para configurações do usuário"""
    try:
        if request.method == 'POST':
            # Aqui iremos processar as configurações do usuário
            messages.success(request, 'Configurações atualizadas com sucesso!')
            return redirect('users:settings')
            
        return render(request, 'users/settings.html')
        
    except Exception as e:
        messages.error(request, f'Erro ao atualizar configurações: {str(e)}')
        return render(request, 'users/settings.html')