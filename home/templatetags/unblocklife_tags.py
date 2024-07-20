from django import template
from wagtail.models import Page
from home.models import UnblocklifeLogo, UnblocklifeThankyou 

register = template.Library()

@register.simple_tag
def unblocklifelogo():
   return UnblocklifeLogo.objects.first();

@register.simple_tag
def unblocklifethankyou():
   return UnblocklifeThankyou.objects.first();



@register.inclusion_tag("tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    self = context.get("self")
    if self is None or self.depth <= 2:
        # When on the home page, displaying breadcrumbs is irrelevant.
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(self, inclusive=True).filter(depth__gt=1)
    return {
        "ancestors": ancestors,
        "request": context["request"],
    }

