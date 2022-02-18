from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, DetailView
from django.views import generic
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
     get_user_model, logout as auth_logout,
)
from .forms import UserCreateForm, UserChangeForm
from concept.models import *
from django.views.generic import FormView
from django.contrib import messages
from django.db.models import Q
from . import forms
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings
import stripe 
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.ENDPOINT_SECRET

class TopArtView(TemplateView):
  template_name = "top.html"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    art_list = Art.objects.all()
    context["art_list"] = art_list
    return context

##def top(request):
    context = {
        'art_list':Art.objects.all(),
    }
    return render(request, 'top.html', context)

class ArtDetail(DetailView):
  model= Art
  template_name = 'art_detail.html'
 


class ArtistDetail(DetailView):
  model= Artist
  template_name = 'artist_detail.html'

def followPlace(request, pk):
    """場所をお気に入り登録する"""
    art = get_object_or_404(Art, pk=pk)
    request.user.favorite_place.add(art)
    return redirect('top')

def RemoveView(request, pk):
    """場所をお気に入り解除する"""
    art = get_object_or_404(Art, pk=pk)
    request.user.favorite_place.remove(art)
    return redirect('top')

class UserDetail(DetailView):
  model= CustomUser
  template_name = 'user_detail.html'

class SignUpView(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserDeleteView(generic.DeleteView):
  template_name = "registration/delete.html"
  success_url = reverse_lazy("top")
  model = CustomUser
  slug_field = 'username'
  slug_url_kwarg = 'username'

class UserChangeView(LoginRequiredMixin, FormView):
    template_name = 'registration/change.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('top')
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'email' : self.request.user.email,
            'first_name' : self.request.user.first_name,
            'last_name' : self.request.user.last_name,
        })
        return kwargs

def followPeople(request, pk):
    """アーティストをお気に入り登録する"""
    artist = get_object_or_404(Artist, pk=pk)
    request.user.favorite_people.add(artist)
    return redirect('top')

def search(request):
    art = Art.objects.order_by('-id')
    keyword = request.GET.get('keyword')
    if keyword:
      art = art.filter(
        Q(artname__icontains=keyword) | Q(artist__artistname__icontains=keyword)
        )
      messages.success(request, '「{}」の検索結果'.format(keyword))
    return render(request, 'search.html', {'art': art })

class ContactView(generic.FormView):
  template_name = "contact.html"
  form_class = forms.ContactForm
  success_url = reverse_lazy('top')

  def form_valid(self,form):
    form.send_email()
    return super().form_valid(form)  


def Returndef(request, pk):
    returnlist = Return.objects.filter(artist__id=pk)
    return render(request, 'return.html', {'returnlist': returnlist})

#以下追記02.15　決済

def checkout_success_view(request):
    return render(request, 'kessai.html')

@require_POST
def create_checkout_session(request):
    return_id = request.POST.get('return')
    returns = get_object_or_404(Return, id=return_id)
    # customer = request.user

    session = stripe.checkout.Session.create(
        # customer_email= customer.email,
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'jpy',
                'product_data': {
                    'name': returns.returnname,
                    #'images': [returns.image.url]
                },
                'unit_amount': returns.lank.price,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.scheme + '://' + request.get_host() + reverse('kessai'),
        cancel_url=request.scheme + '://' + request.get_host() + reverse('top'),
        metadata = {
            'product_id': returns.id,
        }
    )
    return redirect(session.url)

@csrf_exempt
@require_POST
def checkout_success_webhook(request):
  payload = request.body.decode('utf-8')
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
     )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']

    Order.object.create(
    product = Return.objects.get(id=1),
    price = 200,
    stripe = 2
    )
    print("Fulfilling order")
    return HttpResponse(status=200)

def fulfill_order(session):
  order = Order.object.create(
    product = Return.objects.get(id=session['metadata']['product_id']),
    price = session['amount_total'],
    stripe = session['id']
   )
  print("Fulfilling order")