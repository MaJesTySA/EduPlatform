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
4. 注册成功发送邮件之后，会跳转到登录页面，并弹出邮件提示框。并且在用户名处会自动填写注册的邮箱。
<div align="center">
    <img src="https://raw.githubusercontent.com/MaJesTySA/EduPlatform/master/imgs/login.png" width="70%"/>
</div>