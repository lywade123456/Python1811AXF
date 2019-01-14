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
def market(request):
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
    goods_list = Goods.objects.filter(categoryid=categoryid)

    data = {
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'childtypes': childtypes
    }

    return render(request, 'market/market.html',context=data)


def cart(request):
    return render(request, 'cart/cart.html')


def mine(request):
    return render(request, 'mine/mine.html')