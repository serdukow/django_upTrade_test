from django import template
from django.urls import reverse_lazy, NoReverseMatch
from menu.models import Child
from django.db.models import Q

register = template.Library()


@register.inclusion_tag('menu/base.html', takes_context=True)
def draw_menu(context, menu_name):
    request_url = context['request'].build_absolute_uri()
    menu_items = Child.objects.filter(Q(menu_name=menu_name) & Q(parent__isnull=False))
    items_dict = {}
    for item in menu_items:
        try:
            item_url = item.href or context['request'].build_absolute_url(reverse_lazy(item.named_url))
        except NoReverseMatch:
            item_url = None
        items_dict[item.id] = {
            'menu_name': menu_name,
            'item_id': item.id,
            'title': item.title,
            'parent_id': item.parent_id,
            'href': item_url,
            'expand': False,
            'children': []
        }
        if request_url.endswith(str(item_url)):
            items_dict[item.id]['expand'] = True

    root_items = []
    for item_id, item_value in items_dict.items():
        item_parent = item_value['parent_id']
        if item_parent is not None:
            items_dict[item_parent]['children'].append(item_value)
        else:
            root_items.append(item_value)

    return {'menu_parts': root_items, 'menu_name': menu_name}


@register.inclusion_tag('menu/menu_parts.html')
def menu_parts(items):
    return {'items': items}

