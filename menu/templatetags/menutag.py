from django import template
from menu.models import Menu
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_title):
    current_url = context.get('current_url', '')
    menu = Menu.objects.get(title=menu_title)
    children_items = menu.children.all()
    menu_html = '<ul>'

    menu_html += '<li>'
    if current_url == menu.url:
        menu_html += f'<a href="{menu.url}"><strong>{menu.title}</strong></a>'
    else:
        menu_html += f'<a href="{menu.url}">{menu.title}</a>'

    if menu.parent != None:
        parent_html = draw_ancestors(menu)
        menu_html = parent_html + menu_html

    submenu_html = draw_submenu(current_url, children_items)
    if submenu_html:
        menu_html += submenu_html

        menu_html += '</li>'
    menu_html += '</ul>'

    return mark_safe(menu_html)


def draw_submenu(current_url, submenu_items):
    if not submenu_items:
        return ''

    submenu_html = '<ul>'
    for item in submenu_items:
        submenu_html += '<li>'
        if current_url == item.url:
            submenu_html += f'<a href="{item.url}" class="active">{item.title}</a>'
        else:
            submenu_html += f'<a href="{item.url}">{item.title}</a>'

        submenu_html += '</li>'
    submenu_html += '</ul>'

    return mark_safe(submenu_html)


def draw_ancestors(item):
    ancestors = []
    while item.parent:
        ancestors.append(item.parent)
        item = item.parent
    ancestors.reverse()

    ancestors_html = ''
    for ancestor in ancestors:
        ancestors_html += f'<ul><li><a href="{ancestor.url}">{ancestor.title}</a></li>'
    return mark_safe(ancestors_html)
