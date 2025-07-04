from django.core.paginator import Paginator


def get_page_obj(request, posts):
    posts_list = posts
    paginator = Paginator(posts_list, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj