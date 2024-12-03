from django import template

register = template.Library()

@register.inclusion_tag('tasks/recursive_droppable.html')
def render_droppable_structure(sub_function):
    return {
        'sub_function': sub_function,
        'children': sub_function.children.all()
    }


@register.inclusion_tag('tasks/recursive_draggable.html')
def render_draggables(sub_function):
     return {
        'sub_function': sub_function,
        'children': sub_function.children.all()
    }