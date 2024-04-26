# views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from jsonschema import ValidationError
from .models import Kiralanan, İHA
from rest_framework import serializers, viewsets, filters
from .models import İHA, Kiralanan
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.http import JsonResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'redirect_url': '/anasayfa'})  # Başarılı giriş, anasayfaya yönlendir
    return render(request, 'login.html')



def register_view(request):
    if request.method == 'POST':
        # POST verilerini alın
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Kullanıcı oluşturun
        user = User.objects.create_user(username=username, email=email, password=password)
        # Kullanıcıyı kaydedin
        user.save()
        # Kayıt başarılı, giriş sayfasına yönlendir
        return redirect('login')
    else:
        # GET isteği ise, boş bir form gösterin
        return render(request, 'register.html')
    
@login_required
def anasayfa_view(request):
    return render(request, 'anasayfa.html')

@login_required
def iha_ekle_view(request):
    if request.method == 'POST':
        iha_ad = request.POST.get('ihaAd')
        iha_marka = request.POST.get('ihaMarka')
        iha_model = request.POST.get('ihaModel')
        iha_agirlik = request.POST.get('ihaAgirlik')
        
        İHA.objects.create(
            ihaAd=iha_ad,
            ihaMarka=iha_marka,
            ihaModel=iha_model,
            ihaAgirlik=iha_agirlik
        )
        
        return redirect('anasayfa')  # İHA başarıyla kaydedildi, anasayfa sayfasına yönlendir
    else:
        return render(request, 'iha_ekle.html')
    

@login_required  
def iha_listele_view(request):
    ihalar = İHA.objects.all()
    return render(request, 'iha_listele.html', {'ihalar': ihalar})


@login_required
def iha_guncelle_view(request, iha_id):
    iha = get_object_or_404(İHA, id=iha_id)
    if request.method == 'POST':
        iha.ihaAd = request.POST.get('ihaAd')
        iha.ihaMarka = request.POST.get('ihaMarka')
        iha.ihaModel = request.POST.get('ihaModel')
        iha.ihaAgirlik = request.POST.get('ihaAgirlik')
        iha.save()
        return redirect('iha_listele')
    return render(request, 'iha_guncelle.html', {'iha': iha})


@login_required
def kiralanan_ihalar_listele_view(request):
    kiralanan_ihalar = Kiralanan.objects.all()
    return render(request, 'kiralanan_ihalar_listele.html', {'kiralanan_ihalar': kiralanan_ihalar})


@login_required
def kiralanan_iha_guncelle_view(request, kiralanan_id):
    kiralanan_iha = get_object_or_404(Kiralanan, id=kiralanan_id)
    if request.method == 'POST':
        # POST verilerini al ve ilgili İHA kiralama kaydını güncelle
        kiralanan_iha.ihaAd = request.POST.get('ihaAd')
        kiralanan_iha.ihaMarka = request.POST.get('ihaMarka')
        kiralanan_iha.ihaModel = request.POST.get('ihaModel')
        kiralanan_iha.ihaAgirlik = request.POST.get('ihaAgirlik')
        try:
            kiralanan_iha.full_clean()  # Model alan doğrulamasını gerçekleştir
            kiralanan_iha.save()
            return JsonResponse({'success': True})  # Başarı durumunda JSON yanıtı döndür
        except ValidationError as e:
            errors = dict(e)  # Hata mesajlarını bir sözlüğe dönüştür
            return JsonResponse({'success': False, 'errors': errors}, status=400)  # Hata durumunda JSON yanıtı döndür, 400 status kodu ile
    return render(request, 'kiralanan_iha_guncelle.html', {'kiralanan_iha': kiralanan_iha})


@login_required
def kiralanan_iha_sil_view(request, kiralanan_id):
    kiralanan_iha = get_object_or_404(Kiralanan, id=kiralanan_id)
    if request.method == 'POST':
        kiralanan_iha.delete()
        return redirect('kiralanan_ihalar_listele')
    return render(request, 'kiralanan_iha_sil.html', {'kiralanan_iha': kiralanan_iha})



@login_required
def iha_kirala_view(request):
    if request.method == 'POST':
        iha_id = request.POST.get('iha')
        baslangic_tarihi = request.POST.get('baslangicTarihi')
        bitis_tarihi = request.POST.get('bitisTarihi')
        
        # İHA_Kiralama modeline kayıt ekleme
        Kiralanan.objects.create(
            iha_id=iha_id,
            baslangicTarihi=baslangic_tarihi,
            bitisTarihi=bitis_tarihi
        )
  
        
        return redirect('kiralanan_ihalar_listele')  # Başka bir sayfaya yönlendir
    else:
        ihalar = İHA.objects.all()
        return render(request, 'iha_kirala.html', {'ihalar': ihalar})
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class İHASerializer(serializers.ModelSerializer):
    class Meta:
        model = İHA
        fields = ['id', 'ihaAd', 'ihaMarka', 'ihaModel', 'ihaAgirlik']

class KiralananSerializer(serializers.ModelSerializer):
    kullanici = UserSerializer()
    iha = İHASerializer()

    class Meta:
        model = Kiralanan
        fields = ['id', 'kullanici', 'iha', 'baslangicTarihi', 'bitisTarihi']

class İHAViewSet(viewsets.ModelViewSet):
    queryset = İHA.objects.all()
    serializer_class = İHASerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ihaAd', 'ihaMarka', 'ihaModel']  # Arama alanlarını burada belirtin
    ordering_fields = ['ihaAgirlik']  # Sıralama alanlarını burada belirtin

class KiralananViewSet(viewsets.ModelViewSet):
    queryset = Kiralanan.objects.all()
    serializer_class = KiralananSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['iha__ihaAd', 'kullanici__username']  # Arama alanlarını burada belirtin
    ordering_fields = ['baslangicTarihi', 'bitisTarihi']  # Sıralama alanlarını burada belirtin