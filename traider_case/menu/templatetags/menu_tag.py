from django import template
from django.template import loader
from menu.models import HeadMenu, Menu

register = template.Library()


# В метод передается: пункт меню; список объектов для поиска
# дочерних подпунктов; ветка подпункта которая должна быть раскрыта(если есть);
# сам подпункт который должен быть раскрыт(для сравнения).
def create_menu(p_obj, queryset, child_menu=None, child_activ=None):
    # Формируется список дочерних пунктов.
    childes_obj = []
    for obj in queryset:
        if obj['parent_id'] == p_obj['id']:
            childes_obj.append(obj)

    # Создание ссылки на текущий подпункт.
    temp_link = loader.get_template('link.html')
    parent = temp_link.render({'obj': p_obj})

    # Создание списка ссылок дочерних пунктов. Для пункта,
    # который должен быть раскрыт, вместо ссылки передается ветка.
    childes = []
    for child in childes_obj:
        childes.append(
            child_menu if child == child_activ else temp_link.render(
                {'obj': child},
            ),
        )
    menu_temp = loader.get_template('menu.html')
    return menu_temp.render({'parent': parent, 'childes': childes})


def get_obj(queryset, idx):
    #  Поиск подпункта в списке по id
    for obj in queryset:
        if obj['id'] == idx:
            return obj
    return None


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_title):
    # Проверка, существует ли заданное меню.
    try:
        head = HeadMenu.objects.select_related('menu').get(title=menu_title)
    except HeadMenu.DoesNotExist:
        return f'Menu "{menu_title}" not found'

    # Составление списка подпунктов меню, относящихся к заданному меню.
    queryset = list(Menu.objects.filter(menu_title=head).values())

    # Поиск подпункта меню с url текущей страницы.
    # Если не найден, будет выведена ссылка на само меню.
    for obj in queryset:
        if obj['url'] == context.request.path:
            current_obj = obj
            break
    else:
        temp_link = loader.get_template('link.html')
        return temp_link.render({'obj': head.menu})

    # Составление дерева меню до подпункта с текущим url.
    current_menu = create_menu(current_obj, queryset)
    while current_obj['parent_id'] is not None:
        current_menu = create_menu(
            get_obj(queryset, current_obj['parent_id']),
            queryset,
            current_menu,
            current_obj,
        )
        current_obj = get_obj(queryset, current_obj['parent_id'])
    return current_menu
