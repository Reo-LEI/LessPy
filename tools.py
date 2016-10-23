from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_page(paginator, page):
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result
