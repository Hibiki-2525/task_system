import random
from django import template

register = template.Library()

@register.filter
def shuffle(value):
    """リストをランダムな順序に並べ替える"""
    if isinstance(value, list):
        value = value[:]  # 元のリストを変更しないようコピーを作成
        random.shuffle(value)
    return value
