from django import template

from posts.models import Follow

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter()
def check_follow(user, following):
    follow = Follow.objects.filter(
        user=user.id, following=following.id).exists()
    return follow
