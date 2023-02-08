from base64 import b64encode
from django import template

register = template.Library()

@register.filter
def bin_2_img(bstring):
    if bstring is not None:
        lenmax = len(bstring) - len(bstring)%4
        return b64encode(bstring[0:lenmax]).decode('utf8')