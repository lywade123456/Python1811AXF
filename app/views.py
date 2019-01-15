from django.http import HttpResponse
from django.shortcuts import render

from app.models import Wheel, Nav, Mustbuy, Shop, MainShop, Foodtypes, Goods


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
        'wheels':wheels,
        'navs':navs,
        'mustbuys':mustbuys,
        'shophead':shophead,
        'shoptabs':shoptabs,
        'shopclass':shopclass,
        'shopcommends':shopcommends,
        'mainshows':mainshows
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
    #根据分类下标 获取 分类ID
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
    if childcid == '0':       # 全部分类
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:   # 对应分类下的 子类
        goods_list = Goods.objects.filter(categoryid=categoryid).filter(childcid=childcid)

    # 排序处理
    if sortid == '2':   # 销量排序
        goods_list = goods_list.order_by('-productnum')
    elif sortid == '3': # 价格最低
        goods_list = goods_list.order_by('price')
    elif sortid == '4': # 价格最高
        goods_list = goods_list.order_by('-price')

    data = {
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'childtypes': childtypes,
        'childcid':childcid
    }

    return render(request, 'market/market.html',context=data)


def cart(request):
    return render(request, 'cart/cart.html')


def mine(request):
    return render(request, 'mine/mine.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')
    elif request.method == 'POST':
        pass


def register(request):
    if request.method == 'GET':
        return render(request, 'mine/register.html')
    elif request.method == 'POST':
        print(request.POST.get('name'))

        return HttpResponse('正在注册...')
