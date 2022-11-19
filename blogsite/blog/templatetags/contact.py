from django import template
from blog.models import Category
from blog.forms import ContactForm

register = template.Library()


@register.inclusion_tag('blog/contact_form.html')
def contact_form():
    return {'contact_form': ContactForm()}
