from random import Random
from django.core.mail import send_mail

from MxOnline.settings import EMAIL_FROM
from users.models import EmailVerifyRecord


def random_str(randomlength=8):
    _str = ''
    chars = 'AaBbCcDdEeFfGgHh'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        _str += chars[random.randint(0, length)]
    return _str


def send_register_email(email, send_type="register"):
    code = random_str(5)
    EmailVerifyRecord.objects.create(send_type=send_type, email=email, code=code)

    if send_type == "register":
        email_title = "慕雪在线网注册激活链接"
        email_body = f"点击链接激活账号: http://127.0.0.1:21212/active/{code}"
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == "forget":
        email_title = "慕雪在线网reset"
        email_body = f"点击链接激活账号: http://127.0.0.1:21212/reset/{code}"
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == "update_email":
        email_title = "慕雪在线网修改邮箱验证码"
        email_body = f"您的邮箱验证码为 : {code}"
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
