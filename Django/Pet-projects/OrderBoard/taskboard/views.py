from audioop import reverse
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView
from .models import OrderPetition, AdvUser
from .forms import RegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect


def index(request):
    orders = OrderPetition.objects.filter(status__exact="E").order_by('order_time').reverse()[:4]
    in_working = OrderPetition.objects.filter(status__exact="W").count()
    context = {
        'orders': orders,
        'in_working': in_working,
    }
    return render(request, 'index.html', context=context)


class UserCreate(CreateView):
    # Модель куда выполняется сохранениеs
    model = AdvUser
    # Класс на основе которого будет валидация полей
    form_class = RegisterForm

    template_name = 'registration/user_create.html'

    success_url = '/accounts/login/'


class OrdersByUserListView(LoginRequiredMixin, ListView):
    model = OrderPetition
    template_name = 'orders/user_orders.html'
    paginate_by = 10
    context_object_name = 'order_list'

    def get_queryset(self):
        return (
            OrderPetition.objects.filter(user_id=self.request.user).order_by('order_time').reverse()
        )




class OrderDelete(PermissionRequiredMixin, DeleteView):
    model = OrderPetition
    success_url = '/my-orders/'
    permission_required = 'delete_order'
    template_name = 'order_delete_form.html'
    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
            reverse("application-delete", kwargs={"pk": self.object.pk})
            )