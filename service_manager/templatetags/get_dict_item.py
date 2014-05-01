from django import template

register = template.Library()

@register.filter()
def get_dict_item(dict, key):
    """
    Custom filter to get an item from dictionary. Returns None if key doesn't exist
    """
    value = dict.get(key)
    if value is None:
        return 'Folder'
    else:
        return value