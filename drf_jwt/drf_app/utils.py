from django.utils import timezone
import uuid



def define_exp_date():
    return (timezone.now() + timezone.timedelta(days=30)).date()


def gen_ref_code():
    return str(uuid.uuid4())