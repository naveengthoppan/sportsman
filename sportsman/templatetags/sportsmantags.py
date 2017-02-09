from django import template
register = template.Library()

def event_tags(events):
    return ', '.join(events)

register.filter('event_tags', event_tags)