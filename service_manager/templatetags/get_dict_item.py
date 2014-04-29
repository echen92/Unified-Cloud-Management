from django import template

register = template.Library()

@register.filter()
def get_dict_item(dict, key):
    """
    Filter to get item from dictionary
    """
    value = dict.get(key)
    if value is None:
        return 'Folder'
    else:
        return value