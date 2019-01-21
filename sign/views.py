from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request): # 创建路由匹配的视图函数
    return render(request, 'index.html')
# 登录动作
def login_action(request):
    # 获取并判断登录方式
    if request.method == 'POST':
        # 根据html标签的name属性获取数据，获取post请求，在获取用户名与密码
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username  # 将session信息记录到浏览器
            # response.set_cookie('user', username, 3600) # 添加浏览器cookie
            # 对路径进行重定向
            response = HttpResponsePermanentRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error':'username or password error'})

# 发布会管理
@login_required # 限制该视图必须登录后才能访问
def event_manage(request):
    # username = request.COOKIES.get('user', '') # 读取浏览器cookie
    username = request.session.get('user', '') # 读取浏览器session
    return render(request, 'event_manage.html', {'user':username})

