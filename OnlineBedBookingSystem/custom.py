import random2
import string
from django.utils.text import slugify
from django.core.mail import send_mail
from .settings import EMAIL_HOST_USER


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random2.choice(chars) for _ in range(size))


def unique_slug_generator_through_name(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)
    klass = instance.__class__

    if klass.objects.filter(slug=slug).exists():
        new_slug = "{slug}-{randstr}".format(slug=slug, randstr=random_string_generator(size=4))
        return unique_slug_generator_through_name(instance, new_slug=new_slug)
    return slug


def unique_room_genarator(instance):
    id = ''
    klass = instance.__class__
    while True:
        id = random_string_generator()

        if klass.objects.filter(unique_room_id=id).exists():
            continue
        else:
            break
    
    return id



def send_mail_to_customer(subject, message, email):
    mail_subject = subject
    mail_message = message
    to_email = [email]
    from_email_username = 'BookYourBed <{}>'.format(EMAIL_HOST_USER)

    send_mail(
        subject=mail_subject,
        message=mail_message,
        from_email=from_email_username,
        recipient_list=to_email,
        fail_silently=False
    )


