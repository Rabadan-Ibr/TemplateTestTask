from django import template
from django.template import loader
from menu.models import HeadMenu, Menu

register = template.Library()


def create_menu(obj, child_menu=None, child_activ=None):
    childes_obj = obj.childes.all()
    temp_link = loader.get_template('link.html')
    parent = temp_link.render({'obj': obj})
    childes = []
    for child in childes_obj:
        childes.append(
            child_menu if child == child_activ else temp_link.render(
                {'obj': child},
            ),
        )
    menu_temp = loader.get_template('menu.html')
    return menu_temp.render({'parent': parent, 'childes': childes})


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_title):
    try:
        head = HeadMenu.objects.get(title=menu_title)
    except HeadMenu.DoesNotExist:
        return f'Menu "{menu_title}" not found'
    try:
        current_obj = Menu.objects.get(url=context.request.path)
    except Menu.DoesNotExist:
        temp_link = loader.get_template('link.html')
        return temp_link.render({'obj': head.menu})
    current_menu = create_menu(current_obj)
    while current_obj.parent is not None:
        current_menu = create_menu(
            current_obj.parent,
            current_menu,
            current_obj,
        )
        current_obj = current_obj.parent
    return current_menu
