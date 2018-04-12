from django import template

register = template.Library()

@register.inclusion_tag('comChildren.html')
def com_children_tag(comment):
    children = comment.comkids.all
    return {'children': children}
