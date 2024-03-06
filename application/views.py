from django.shortcuts import render
from django.http import JsonResponse
import smtplib
from email.message import EmailMessage
from .models import *

def checkID(ARR1, ARR2, quality):
    posts = WebPost.objects.all()
    posts_categories = WebPostCategories.objects.all()
    for postCat in posts_categories:
        if postCat.name.id != quality:
            continue # пропускаем пост
        else:
            ARR1.append(postCat.post.id)

    for post in posts:
        if post.id not in ARR1:
            continue # пропускаем пост
        else:
            ARR2.append(post) 
    return ARR2

# Create your views here.
def index_page(request):
    products = Product.objects.all()

    AllUnit = []
    MainUnit_ = []
    checkID(AllUnit, MainUnit_, 1)
    MainUnit_ = sorted(MainUnit_, key=lambda x: x.created_date, reverse=True)     

    AllUnit = []
    RSideUnit_ = []
    checkID(AllUnit, RSideUnit_, 2)
    RSideUnit_ = sorted(RSideUnit_, key=lambda x: x.created_date, reverse=True)     

    AllUnit = []
    LatestUnit_ = []
    checkID(AllUnit, LatestUnit_, 4)
    LatestUnit_ = sorted(LatestUnit_, key=lambda x: x.created_date, reverse=True)     

    context = {
        'products': products,
        'MainUnit': MainUnit_,
        'RSideUnit': RSideUnit_,
        'LatestUnit': LatestUnit_,
    }
    return render(request, 'index.html', context)

def catalog_page(request):
    topRatedCategory_ = Product.objects.all()
    filteredProduct_ = Product.objects.all()
    filterCategory_ = Categories.objects.all()
    filterColor_ = Color.objects.all()
    filterMaterial_ = MaterialType.objects.all()
    filterSize_ = SizeCatalog.objects.all()

    PromoNews = []
    PromoNews_ = []
    checkID(PromoNews, PromoNews_, 3)
    PromoNews_ = sorted(PromoNews_, key=lambda x: x.created_date, reverse=True) 

    context = {
        'topRatedCategory': topRatedCategory_,
        'filteredProduct': filteredProduct_,
        'filterCategory': filterCategory_,
        'filterColor': filterColor_,
        'filterMaterial': filterMaterial_,
        'filterSize': filterSize_,
        'promoNews': PromoNews_,
    }
    return render(request, 'catalog.html', context)

def filter_data(request):

    selected_categories = request.GET.getlist('Categories')
    selected_color = request.GET.getlist('Color')
    selected_size = request.GET.getlist('sizes')
    selected_stuff = request.GET.getlist('stuff')

    filter_price1 = request.GET.get('min_price')
    filter_price2 = request.GET.get('max_price')

    filtered_Product = Product.objects.all()
    filtered_Sizes = Sizes.objects.all()
    filtered_Stuffs = Stuff.objects.all()
    filtered_Images = Images.objects.all()
    filtered_Tag = Tag.objects.all()
    
    products_list = []

    dimension_catalog = []
    dimension_detail = []

    texture_catalog = []
    texture_detail = []
    picture_detail = []
    tags_detail = []

    for product in filtered_Sizes:
        
        if str(product.name.id) not in selected_size:
            continue # пропускаем товары

        if product.product.id not in dimension_catalog:
            dimension_catalog.append(product.product.id)

    for product in filtered_Stuffs:
        
        if str(product.name.id) not in selected_stuff:
            continue # пропускаем товары

        if product.product.id not in texture_catalog:
            texture_catalog.append(product.product.id)

    for product in filtered_Product:

        dimension_detail = []
        texture_detail = []
        picture_detail = []
        tags_detail = []

        if int(product.price) < int(filter_price1) or int(product.price) > int(filter_price2):
            continue # пропускаем товары

        if len(dimension_catalog) == 0:
            pass
        else:
            if product.id not in dimension_catalog:
                continue # пропускаем товары

        if len(texture_catalog) == 0:
            pass
        else:
            if product.id not in texture_catalog:
                continue # пропускаем товары

        if len(selected_categories) == 0:
            pass
        else:
            if str(product.Categories.id) not in selected_categories:
                continue # пропускаем товары

        if len(selected_color) == 0:
            pass
        else:   
            if str(product.Color.id) not in selected_color:
                continue # пропускаем товары

        for metering in filtered_Sizes:

            if metering.product.id != product.id:
                continue
            
            dimension_detail.append(str(metering.name))

        for fabric in filtered_Stuffs:

            if fabric.product.id != product.id:
                continue
            
            texture_detail.append(str(fabric.name))

        for picture in filtered_Images:

            if picture.product.id != product.id:
                continue

            picture_detail.append('media/' + str(picture.image))

        for tags in filtered_Tag:

            if tags.product.id != product.id:
                continue

            tags_detail.append(str(tags.name))

        product_dict = {
            'id': product.id,
            'unique_id': product.unique_id,
            'name': product.name,
            'image': 'media/' + product.image.name,
            'saleprice': product.saleprice,
            'price': product.price,
            'condition': product.condition,
            'сategories': product.Categories.name,
            'color': product.Color.name,
            'short_description': product.short_description,
            'description': product.description,
            'сare_instructions': product.сare_instructions,
            'created_date': product.created_date,
            'dimension': dimension_detail,
            'texture': texture_detail,
            'pictures': picture_detail,
            'tags': tags_detail,
        }
        products_list.append(product_dict)
    
    # Возвращаем отфильтрованные данные в формате JSON
    data = {'data': list(products_list)}
    return JsonResponse(data, safe=False)

def detail_page(request, id):
    prod = Product.objects.filter(unique_id = id).first()
    similarProd = Product.objects.all()
    lastaddProd = Product.objects.all()


    context = {
        'prod': prod,
        'similarProd': similarProd,
        'lastaddProd': lastaddProd,
    }
    return render(request, 'item-details.html', context)

def gallery_page(request):
    products = Product.objects.all()
    TrendsPosts = Product.objects.all()
    ModatelGallery = Product.objects.all()
    SportStyleGallery = Product.objects.all()
    LastAddedGallery = Product.objects.all()
    context = {
        'products': products,
        'TrendsPosts': TrendsPosts,
        'ModatelGallery': ModatelGallery,
        'SportStyleGallery': SportStyleGallery,
        'LastAddedGallery': LastAddedGallery,
    }
    return render(request, 'gallery.html', context)

def blog_page(request):
    products = Product.objects.all()

    postsMV = WebPost.objects.all().order_by('-views')
    postsLST = WebPost.objects.all().order_by('-created_date')

    AllUnit = []
    MainUnit_ = []
    checkID(AllUnit, MainUnit_, 1)
    MainUnit_ = sorted(MainUnit_, key=lambda x: x.created_date, reverse=True)  

    AllUnit = []
    RSideUnit_ = []
    checkID(AllUnit, RSideUnit_, 2)
    RSideUnit_ = sorted(RSideUnit_, key=lambda x: x.created_date, reverse=True) 

    AllUnit = []
    PromoNews_ = []
    checkID(AllUnit, PromoNews_, 3)
    PromoNews_ = sorted(PromoNews_, key=lambda x: x.created_date, reverse=True) 

    #AllUnit = []
    #posts_MainNews_ = []

    #AllUnit = []
    #posts_LSBarNews_ = []

    #AllUnit = []
    #posts_RSBarNews_ = []

    #AllUnit = []
    #posts_PromNews_ = []

    #AllUnit = []
    #posts_LastNews_ = []

    #checkID(AllUnit, posts_MainNews_, 4)
    #checkID(AllUnit, posts_LSBarNews_, 6)
    #checkID(AllUnit, posts_RSBarNews_, 5)
    #checkID(AllUnit, posts_PromNews_, 7)
    #checkID(AllUnit, posts_LastNews_, 7)

    context = {
        'products': products,
        'MainUnit': MainUnit_,
        'RSideUnit': RSideUnit_,
        'PromoNews': PromoNews_,
        'postsMV': postsMV,
        'postsLST': postsLST,
    }
    return render(request, 'blog.html', context)

def post_page(request, id):
    posts = WebPost.objects.filter(unique_id = id).first()
    post_view = WebPost.objects.get(unique_id = id)

    postsLST = WebPost.objects.all().order_by('-views')

    post_view.views += 1

    post_view.save()

    context = {
        'posts': posts,
        'post_view': post_view,
        'postsLST': postsLST,
    }
    return render(request, 'item-post.html', context)

def about_us_page(request):

    return render(request, 'about_us.html')

def PrivPol_page(request):

    return render(request, 'privPol.html')

def contacts_page(request):

    return render(request, 'contacts.html')

def send_email(request):
    if request.method == 'POST':
        from_email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = from_email + ' is typing:' '\n' + request.POST.get('message')
        email = EmailMessage()
        email['from'] = 'modatelru@gmail.com'  # Замените на ваш Gmail адрес
        email['to'] = 'modatelru@gmail.com'
        email['subject'] = subject
        email.set_content(message)
        
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login('modatelru@gmail.com', 'ncvu ialo xhnx pgry')  # Замените на ваш Gmail адрес и пароль
        smtp.send_message(email)
        smtp.quit()
        
        return render(request, 'email_form.html')