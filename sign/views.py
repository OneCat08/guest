from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
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
    event_list = Event.objects.all() #查询所有发布会的数据
    # username = request.COOKIES.get('user', '')  # 读取浏览器cookie
    username = request.session.get('user', '')  # 读取浏览器session
    return render(request, 'event_manage.html', {'user': username,
                                                 'events': event_list})  # 返给客户端

# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {'user': username,
                                                 'events': event_list})
# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()  # 查询Guest表的所有数据
    paginator = Paginator(guest_list, 2)  # 创建每页2条数据的分页器
    page = request.GET.get('page')  # 通过get请求得到当前要显示第几页的数据
    try:
        contacts = paginator.page(page)  # 获取页面数据
    except PageNotAnInteger:
        # 如果page不是整数，取第一页面的数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围，取最后一页的数据
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {'user': username,
                                                 'guests': contacts})

# 签到页面
@login_required
def sign_index(request, eid):  # 获取URL配置得到eid，作为发布会的id查询条件
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})

# 签到动作
@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'phone error.'})
    result = Guest.objects.filter(phone=phone, event_id=eid)

    if not result:
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'event id or phone error.'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return  render(request, 'sign_index.html', {'event': event,
                                                    'hint': 'user has sign in.'})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   'hint': 'sign in success!',
                                                   'guest': result})

# 退出登录
@login_required
def logout(request):
    auth.logout(request)  # 退出登录
    response = HttpResponsePermanentRedirect('/index/')
    return response