from random import Random

from EduPlatform.settings import EMAIL_FROM
from users.models import EmailVerifyRecord
from django.core.mail import send_mail


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    random_str = generate_random_str(16)
    if send_type=='update_email':
        random_str=generate_random_str(4)

    email_record.code = random_str
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '注册激活连接'
        email_body = '请点击下面的链接激活账号：http://127.0.0.1:8000/active/{0}'.format(random_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '密码重置连接'
        email_body = '请点击下面的链接重置密码：http://127.0.0.1:8000/reset/{0}'.format(random_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'update_email':
        email_title = '修改邮箱连接'
        email_body = '你的邮箱验证码为：{0}'.format(random_str)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

def generate_random_str(random_len=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_len):
        str += chars[random.randint(0, length)]
    return str
