from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:user_read'))
    else:
        user_form = ShopUserRegisterForm()
    content = {
        'form': user_form
    }
    return render(request, 'adminapp/user_update.html', content)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     users_list = ShopUser.objects.all().order_by('is_active', '-is_superuser', '-is_staff', 'username')
#     content = {
#         'objects': users_list
#     }
#     return render(request, 'adminapp/users.html', content)

class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:user_read'))
    else:
        user_form = ShopUserAdminEditForm(instance=edit_user)

    content = {
        'form': user_form
    }
    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user_item = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        if user_item.is_active:
            user_item.is_active = False
        else:
            user_item.is_active = True
        user_item.save()
        return HttpResponseRedirect(reverse('admin:user_read'))
    content = {
        'user_to_delete': user_item
    }
    return render(request, 'adminapp/user_delete.html', content)


# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     pass
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:category_read')
    fields = '__all__'
    # form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'
    categories_list = ProductCategory.objects.all()
    content = {
        'title': title,
        'objects': categories_list
    }
    return render(request, 'adminapp/categories.html', content)


# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     title = 'категории/редактирование'
#
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin:category_update', args=[edit_category.pk]))
#     else:
#         edit_form = ProductCategoryEditForm(instance=edit_category)
#     content = {
#         'title': title,
#         'edit_form': edit_form
#     }
#     return render(request, 'adminapp/category_update.html', content)

class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('adminapp:categories')
    fields = '__all__'
    # form_class = ProductCategoryEditForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'редактирование категорий'
        return context

    def get_success_url(self):
        self.object = self.get_object()
        if self.object.is_active:
            return self.success_url
        return reverse_lazy('adminapp:categories')

class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('adminapp:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(reverse(self.success_url))

# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request):
#     title = 'категории/удаление'
#     category = get_object_or_404(ProductCategory, pk=pk)
#
#     if request.method == 'POST':
#         category.is_active = False
#         category.save()
#         return HttpResponseRedirect(reverse('admin:categories'))
#
#     content = {
#         'title': title,
#         'category_to_delete': category
#     }
#     return render(request, 'adminapp/category_delete.html', content)


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#     else:
#         product_form = ProductEditForm()
#     content = {
#         'form': product_form,
#         'category': category_item
#     }
#     return render(request, 'adminapp/product_update.html', content)

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_update.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['category'] = category
        return context

    def get_success_url(self):
        return reverse('adminapp:products', args=[self.kwargs['pk']])


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk, page=1):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category=category_item).order_by('is_active')
#
#     # paginator = Paginator(products_list, 2)
#
#     # try:
#     #     products_paginator = paginator.page(page)
#     # except PageNotAnInteger:  # если пользователь ввёл непонятное значение, выведется 1 стр
#     #     products_paginator = paginator.page(1)
#     # except EmptyPage:  # если пользователь ввёл большое значение, выведется последняя стр
#     #     products_paginator = paginator.page(paginator.num_pages)
#
#     content = {
#         'products': products_list,
#         'category': category_item
#     }
#     return render(request, 'adminapp/products.html', content)

class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 2

    def get_queryset(self):
        category_pk = self.kwargs['pk']
        return Product.objects.filter(category__pk=category_pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['category'] = category
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     content = {
#         'object': product_item
#     }
#     return render(request, 'adminapp/product_detail.html', content)


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     edit_product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         update_form = ProductEditForm(request.POST, request.FILES,
#                                       instance=edit_product)  # instance указывает на то, что товар будет редактироваться, а не создаваться новый
#         if update_form.is_valid():
#             update_form.save()
#             return HttpResponseRedirect(reverse('adminapp:products', args=[edit_product.category_id]))
#     else:
#         update_form = ProductEditForm(instance=edit_product)
#     content = {
#         'form': update_form,
#         'category': edit_product.category
#     }
#     return render(request, 'adminapp/product_update.html', content)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductEditForm
    template_name = 'adminapp/product_update.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        category = get_object_or_404(ProductCategory, pk=self.object.category.pk)
        context['category'] = category
        return context

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('adminapp:products', args=[self.object.category.pk])


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     product_item = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         product_item.is_active = False
#         product_item.save()
#         return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#
#     content = {
#         'product_to_delete': product_item
#     }
#     return render(request, 'adminapp/product_delete.html', content)
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        self.object = self.get_object()
        return reverse('adminapp:products', args=[self.object.category.pk])