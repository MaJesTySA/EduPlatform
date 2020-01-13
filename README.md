# EduPlatform

主要记录慕课网`Django打造在线教育平台`学习过程，在此基础上做一些优化和修改。

## 2020-1-7

### 主要优化了注册、登录逻辑

1. 现在注册、登录页面的轮播图不再是静态的，而是动态加载的。
2. 注册的时候需要输入两次密码。
<div align="center">
    <img src="https://raw.githubusercontent.com/MaJesTySA/EduPlatform/master/imgs/register1.png" width="70%"/>
</div>
3. 注册时如果格式错误（比如密码），正确的项目（比如邮箱、昵称）会在重新输入时保留。
<div align="center">
    <img src="https://raw.githubusercontent.com/MaJesTySA/EduPlatform/master/imgs/register2.png" width="40%"/>
</div>
4. 注册成功发送邮件之后，会跳转到邮箱发送成功页面，而不是直接跳转到登录框。只有点击验证连接后，才会跳转到登录页面，弹出提示框“激活成功”。并且在用户名处会自动填写注册的邮箱。
<div align="center">
    <img src="https://raw.githubusercontent.com/MaJesTySA/EduPlatform/master/imgs/login.png" width="70%"/>
</div>
5. 优化邮箱激活逻辑。现在激活后，会删除表中数据。

   ```python
   class ActiveUserView(View):
    def get(self, request, active_code):
        try:
            record = EmailVerifyRecord.objects.get(code=active_code)
            email = record.email
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
            record.delete()
            return redirect('/login?email=' + email)
        except Exception:
            return render(request, 'active_fail.html')
   ```

## 2020-1-13

### 主要优化了找回密码逻辑

1. 从`register.html`、`login.html`等页面中提取出了公共部分`register_base.html`。这些页面直接继承公共页面，删除了大量重复代码。

2. 现在重设密码页面`password_reset.html`也继承公共页面，使得风格与登录页面类似。
<div align="center">
    <img src="https://raw.githubusercontent.com/MaJesTySA/EduPlatform/master/imgs/resetpwd2.png" width="60%"/>
</div>

3. 现在找回密码页面`forgetpwd.html`的轮播图也是动态加载的。

4. 优化了找回密码的逻辑。
   
   4.1 在发送邮件之前，先判断用户是否存在。
   <div align="center">
    <img src="https://raw.githubusercontent.com/MaJesTySA/EduPlatform/master/imgs/resetpwd1.png" width="60%"/>
</div>

```python
#class ForgetPwdView
def post(self, request):
    forget_pwd_form = ForgetPwdForm(request.POST)
    banner_courses = Course.objects.filter(is_banner=True)[:3]
    if forget_pwd_form.is_valid():
        email = request.POST.get('email')
        user = UserProfile.objects.filter(email=email)
        #检查账户是否存在，不存在则不发送邮箱
        if user:
            send_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form,
                                                          'banner_courses': banner_courses,
                                                          'msg':'账户不存在！'})
    else:
        return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form,
                                                      'banner_courses': banner_courses})
```
   
   4.2 用户重设密码成功后，跳转到登录页面会提示。
   <div align="center">
    <img src="https://raw.githubusercontent.com/MaJesTySA/EduPlatform/master/imgs/resetpwd3.png" width="60%"/>
</div>
  
   4.3 用户重设密码成功之后，数据库会删除记录。
   
   ```python
class ModifyPwdView(View):
    def post(self, request):
        reset_pwd_form = ResetPwdForm(request.POST)
        if reset_pwd_form.is_valid():
            #省略
            user.save()
            #删除数据库记录
            email_record = EmailVerifyRecord.objects.filter(email=email)
            email_record.delete()
            return redirect('/login?type=reset_pwd')
        else:
            #省略
```