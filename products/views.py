from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product, ProductColorVariation, ProductSizeVariation

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def splash_view(request):
    print(request)
    template = 'splash.html'
    context = {}
    return render(request, template, context)

def unavailable_view(request):
    print(request)
    template = 'directory/unavailable.html'
    context = {}
    return render(request, template, context)

class ProductListView(ListView):
    model = ProductColorVariation
    template_name = 'products/list_view.html'
    paginate_by = 12

class ProductDetailView(DetailView):
    model = ProductColorVariation
    template_name = 'products/detail_view.html'

class MensListView(ListView):
    model = Product
    template_name = 'products/mens_list_view.html'
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        queryset = super(MensListView, self).get_queryset(*args, **kwargs).filter(gender = 'Mens')
        return queryset

class WomensListView(ListView):
    model = Product
    template_name = 'products/womens_list_view.html'
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        queryset = super(WomensListView, self).get_queryset(*args, **kwargs).filter(gender = 'Womens')
        return queryset

class ShoesListView(ListView):
    model = Product
    template_name = 'products/shoes_list_view.html'
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        queryset = super(ShoesListView, self).get_queryset(*args, **kwargs).filter(product_type = 'Shoe')
        return queryset

class AccessoriesListView(ListView):
    model = Product
    template_name = 'products/accessories_list_view.html'
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        queryset = super(AccessoriesListView, self).get_queryset(*args, **kwargs).filter(Q(product_type = 'Hat') | Q(product_type = 'Accessory'))
        return queryset

class CollectionsListView(ListView):
    model = Product
    template_name = 'products/collections_list_view.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(CollectionsListView, self).get_context_data(**kwargs)
        products = Product.objects.filter()
        paginator = Paginator(products, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            paginated_products = paginator.page(page)
        except PageNotAnInteger:
            paginated_products = paginator.page(1)
        except EmptyPage:
            paginated_products = paginator.page(paginator.num_pages)

        context['object_list'] = paginated_products
        return context

def sort_list_view(request):
    # model = Product
    # template_name = 'products/filter_list_view.html'
    # type_filter = request.GET.get('type_filter')
    # queryset_filter(type_filter)()

    template = 'products/sort_list_view.html'
    sort_option = request.GET.get('sort_option')
    if sort_option == None:
        sort_option = 'name'
    print(sort_option)
    try:
        products = Product.objects.sort_by(sort_option)
    except:
        products = Product.objects.none()
    context = {
        "object_list": products
    }
    print(context)
    return render(request, template, context)

    # def queryset_filter(type_filter):
    #     return {
    #         'tops': tops,
    #         'bottoms': bottoms,
    #         'hats': hats,
    #         'shoes': shoes,
    #         'miscellaneous': miscellaneous,
    #     }.get(type_filter, no_filter)

    # def no_filter(self):
    #     queryset = super(SortView, self).get_queryset(*args, **kwargs)
    #     return queryset
    #
    # def tops(self):
    #     queryset = super(SortView, self).get_queryset(*args, **kwargs).filter(product_type = 'Top')
    #     return queryset
    #
    # def bottoms(self):
    #     queryset = super(SortView, self).get_queryset(*args, **kwargs).filter(product_type = 'Bottom')
    #     return queryset
    #
    # def hats(self):
    #     queryset = super(SortView, self).get_queryset(*args, **kwargs).filter(product_type = 'Hat')
    #     return queryset
    #
    # def shoes(self):
    #     queryset = super(SortView, self).get_queryset(*args, **kwargs).filter(product_type = 'Shoe')
    #     return queryset
    #
    # def miscellaneous(self):
    #     queryset = super(SortView, self).get_queryset(*args, **kwargs).filter(product_type = 'Miscellaneous')
    #     return queryset
