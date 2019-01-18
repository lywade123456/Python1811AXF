import hashlib
import random
import time

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from app.alipay import alipay
from app.models import Wheel, Nav, Mustbuy, Shop, MainShop, Foodtypes, Goods, User, Cart, Order, OrderGoods


def home(request):
    # 轮播图数据
    wheels = Wheel.objects.all()

    # 导航数据
    navs = Nav.objects.all()

    # 每日必购
    mustbuys = Mustbuy.objects.all()

    # 商品部分
    shops = Shop.objects.all()
    shophead = shops[0]
    shoptabs = shops[1:3]
    shopclass = shops[3:7]
    shopcommends = shops[7:11]

    # 商品主体内容
    mainshows = MainShop.objects.all()

    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shophead': shophead,
        'shoptabs': shoptabs,
        'shopclass': shopclass,
        'shopcommends': shopcommends,
        'mainshows': mainshows
    }

    return render(request, 'home/home.html', context=data)


# categoryid 分类ID
# childcid 子类ID
# sortid 排序ID [自己定制， 1综合排序， 2销量排序， 3价格最低， 4价格最高]
def market(request, childcid, sortid):
    # 分类
    foodtypes = Foodtypes.objects.all()

    # 获取 客户端点击的 分类下标  >> typeIndex
    typeIndex = int(request.COOKIES.get('typeIndex', 0))
    # 根据分类下标 获取 分类ID
    categoryid = foodtypes[typeIndex].typeid

    # 获取 对应分类下   子类
    childtypenames = foodtypes[typeIndex].childtypenames
    # 拆分
    childtypes = []
    for item in childtypenames.split('#'):
        # item  >>>>  子类名称:子类ID
        temp = item.split(':')
        dir = {
            'childname': temp[0],
            'childid': temp[1]
        }
        childtypes.append(dir)

    # 商品
    # goods_list = Goods.objects.all()[0:5]
    # goods_list = Goods.objects.filter(categoryid=categoryid)

    # 子类处理
    if childcid == '0':  # 全部分类
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:  # 对应分类下的 子类
        goods_list = Goods.objects.filter(categoryid=categoryid).filter(childcid=childcid)

    # 排序处理
    if sortid == '2':  # 销量排序
        goods_list = goods_list.order_by('-productnum')
    elif sortid == '3':  # 价格最低
        goods_list = goods_list.order_by('price')
    elif sortid == '4':  # 价格最高
        goods_list = goods_list.order_by('-price')

    # 获取购物车信息 [对应用户的]
    token = request.session.get('token')
    carts = []
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user)

    data = {
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'childtypes': childtypes,
        'childcid': childcid,
        'carts': carts
    }

    return render(request, 'market/market.html', context=data)


def cart(request):
    token = request.session.get('token')
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(user=user).exclude(number=0)

        data = {
            'carts': carts
        }

        return render(request, 'cart/cart.html', context=data)
    else:
        return redirect('axf:login')


def mine(request):
    # 获取token
    token = request.session.get('token')

    user = None
    data = {}

    if token:
        user = User.objects.get(token=token)
        orders = Order.objects.filter(user=user)

        data = {
            'user': user,
            'waitpay': orders.filter(status=0).count(),
            'paydone': orders.filter(status=1).count()
        }

    return render(request, 'mine/mine.html', context=data)


def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # 假如账号错误，抛出异常
            user = User.objects.get(email=email)
            if user.password == generate_password(password):  # 成功
                user.token = generate_token()
                user.save()
                request.session['token'] = user.token
                return redirect('axf:mine')
            else:  # 密码错误
                return render(request, 'mine/login.html', context={'err': '密码错误'})
        except:
            return render(request, 'mine/login.html', context={'err': '账号不存在'})


def generate_password(param):
    md5 = hashlib.md5()
    md5.update(param.encode('utf-8'))
    return md5.hexdigest()


def generate_token():
    md5 = hashlib.md5()
    tempstr = str(time.time()) + str(random.random())
    md5.update(tempstr.encode('utf-8'))
    return md5.hexdigest()


def register(request):
    if request.method == 'GET':
        return render(request, 'mine/register.html')
    elif request.method == 'POST':
        user = User()
        user.email = request.POST.get('email')
        user.password = generate_password(request.POST.get('password'))
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')

        # 状态保持
        user.token = generate_token()
        request.session['token'] = user.token

        # 存储数据库
        user.save()

        return redirect('axf:mine')


def checkemail(request):
    email = request.GET.get('email')

    users = User.objects.filter(email=email)
    if users.exists():  # 占用
        return JsonResponse({'msg': '账号被占用！', 'status': 0})
    else:  # 可用
        return JsonResponse({'msg': '账号可以使用!', 'status': 1})


def logout(request):
    request.session.flush()
    return redirect('axf:mine')


def addcart(request):
    # 有token，就知道是谁
    token = request.session.get('token')

    if token:  # 加操作(有登录)
        user = User.objects.get(token=token)
        goodsid = request.GET.get('goodsid')
        goods = Goods.objects.get(pk=goodsid)

        # 第一次操作: 添加一条新记录
        # 后续操作: 只需要修改number

        # 判断该商品是否存在
        carts = Cart.objects.filter(user=user).filter(goods=goods)
        if carts.exists():  # 存在，修改numbner
            cart = carts.first()
            cart.number = cart.number + 1
            cart.save()
        else:  # 添加一条新的记录
            cart = Cart()
            cart.user = user
            cart.goods = goods
            cart.number = 1
            cart.save()

        return JsonResponse({'msg': '{}-添加购物车成功!'.format(goods.productlongname), 'status': 1, 'number': cart.number})

    else:  # 跳转到登录(未登录)
        # 在ajax是不能使用重定向
        # ajax更多就是用于数据的传输(数据交互)

        # 问题: 没有登录，就需要跳转到登录页面；
        # 但在服务端重定向能不能用？   客户端
        # return redirect('axf:login')
        return JsonResponse({'msg': '请登录后操作!', 'status': 0})


def subcart(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)

    goodsid = request.GET.get('goodsid')
    goods = Goods.objects.get(pk=goodsid)

    cart = Cart.objects.filter(user=user).filter(goods=goods).first()
    cart.number = cart.number - 1
    cart.save()

    responseData = {
        'msg': '{}-商品删减成功'.format(goods.productlongname),
        'status': 1,
        'number': cart.number
    }

    return JsonResponse(responseData)


def changecartstatus(request):
    cartid = request.GET.get('cartid')

    cart = Cart.objects.get(pk=cartid)
    cart.isselect = not cart.isselect
    cart.save()

    data = {
        'msg': '状态修改成功',
        'status': 1,
        'isselect': cart.isselect
    }

    return JsonResponse(data)


def changecartall(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)

    # True/False
    isall = request.GET.get('isall')
    if isall == 'true':
        isall = True
    else:
        isall = False

    carts = Cart.objects.filter(user=user).update(isselect=isall)

    data = {
        'msg': '状态修改成功',
        'status': 1,
    }

    return JsonResponse(data)


def generate_identifire():
    tempstr = str(int(time.time())) + str(random.random())
    return tempstr


def generateorder(request):
    token = request.session.get('token')
    user = User.objects.get(token=token)

    # 订单
    order = Order()
    order.user = user
    order.identifier = generate_identifire()
    order.save()

    # 订单商品
    carts = Cart.objects.filter(user=user).filter(isselect=True).exclude(number=0)
    # 只有选中的商品，才是添加到订单中，从购物车中删除
    for cart in carts:
        orderGoods = OrderGoods()
        orderGoods.order = order
        orderGoods.goods = cart.goods
        orderGoods.number = cart.number
        orderGoods.save()

        # 从购物车中删除
        cart.delete()

    data = {
        'msg': '下单成功',
        'status': 1,
        'identifier': order.identifier
    }

    return JsonResponse(data)


def orderdetail(request, identifier):
    order = Order.objects.get(identifier=identifier)

    return render(request, 'order/orderdetail.html', context={'order': order})

@csrf_exempt
def appnotify(request):
    # http://112.74.55.3/axf/returnview/?charset=utf-8&out_trade_no=15477988300.6260414050156342&method=alipay.trade.page.pay.return&total_amount=93.00&sign=oaTJZPDeswBfEbQGkBND8w8DDOWGMdz8lw6TlL25Sp73TZtTBqUBx2vazVi5sI6pFLSgfF%2FRsxsiY20S5UzZeCJ5hfrGXp4NCg6ZpZE%2FWS1CsMnI74lO%2F8ttTx1j%2FzfhrJJuTIHJ503Z1wiDZoXHer91ynI%2FCTLn8W0de2fVhnBi5hTo7MJHJBZQnVQ%2BnFJ73cKBB16xdIJ15ISVUrYYi%2FUGJr2jh%2BllGiiTVm4o0maDuYH3ljuGVxAI4yvP%2BevAfo7B2MK%2F1BW3%2FVu8JRLatEIqeyV2Qk87%2F%2FGRndFRjRDuuZMU8zzix0eg0oKYVeBmfOnRPXhMFAs8dGPedC1D2Q%3D%3D&trade_no=2019011822001416700501217055&auth_app_id=2016091800542542&version=1.0&app_id=2016091800542542&sign_type=RSA2&seller_id=2088102176233911&timestamp=2019-01-18+16%3A08%3A08

    # 获取订单号，并且修改订单状态
    if request.method == 'POST':
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)
        post_dir = {}

        print(body_str)
        print(post_data)
        print(post_data.items())
        for key, value in post_data.items():
            post_dir[key] = value[0]

        out_trade_no = post_dir['out_trade_no']
        print(out_trade_no)

        # 更新状态
        Order.objects.filter(identifier=out_trade_no).update(status=1)

        return JsonResponse({'msg': 'success'})


def returnview(request):

    return redirect('axf:mine')


def pay(request):
    identifier = request.GET.get('identifier')
    order = Order.objects.get(identifier=identifier)

    sum = 0
    for orderGoods in order.ordergoods_set.all():
        sum += orderGoods.goods.price * orderGoods.number

    # 支付地址
    url = alipay.direct_pay(
        subject='MacBookPro - 2019款',  # 支付宝页面显示的标题
        out_trade_no=identifier,  # AXF订单编号
        total_amount=str(sum),  # 订单金额
        return_url='http://112.74.55.3/axf/returnview/'
    )

    # 拼接上支付网关
    alipayurl = 'https://openapi.alipaydev.com/gateway.do?{data}'.format(data=url)

    return JsonResponse({'alipayurl': alipayurl, 'status': 1})


def orderlist(request, status):
    orders = Order.objects.filter(status=status)

    return render(request, 'order/orderlist.html', context={'orders': orders})
