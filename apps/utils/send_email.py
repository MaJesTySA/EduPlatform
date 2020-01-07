from random import Random

from EduPlatform.settings import EMAIL_FROM, SERVER_URL
from users.models import EmailVerifyRecord
from django.core.mail import send_mail


def send_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    random_code = generate_random_code(16)

    if send_type == 'update_email':
        random_code = generate_random_code(4)

    email_record.code = random_code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    if send_type == 'register':
        email_title = 'GMOOC在线学习网—注册激活连接'
        email_body = '请点击下面的连接激活账号：{0}/active/{1}'.format(SERVER_URL, random_code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return True
        else:
            return False
    elif send_type == 'forget':
        email_title = 'GMOOC在线学习网—密码重置连接'
        email_body = '请点击下面的链接重置密码：{0}/reset/{1}'.format(SERVER_URL, random_code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return True
        else:
            return False
    elif send_type == 'update_email':
        email_title = '修改邮箱连接'
        email_body = '你的邮箱验证码为：{0}'.format(random_code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            return True
        else:
            return False


def generate_random_code(random_len=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_len):
        str += chars[random.randint(0, length)]
    return str
