from django.db import models

class Base(models.Model):
    img = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=10)

    class Meta:
        abstract = True


# 轮播图 模型类
class Wheel(Base):
    class Meta:
        db_table = 'axf_wheel'


# 导航 模型类
class Nav(Base):
    class Meta:
        db_table = 'axf_nav'


# 必购 模型类
class Mustbuy(Base):
    class Meta:
        db_table = 'axf_mustbuy'

# 商品部分 模型类
class Shop(Base):
    class Meta:
        db_table = 'axf_shop'

# 商品主体 模型类
# insert into axf_mainshow(trackid,name,img,categoryid,brandname,
# img1,childcid1,productid1,longname1,price1,marketprice1,
# img2,childcid2,productid2,longname2,price2,marketprice2,
# img3,childcid3,productid3,longname3,price3,marketprice3)
class MainShop(models.Model):
    trackid = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=100)
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=100)

    img1 = models.CharField(max_length=100)
    childcid1 = models.CharField(max_length=10)
    productid1 = models.CharField(max_length=10)
    longname1 = models.CharField(max_length=100)
    price1 = models.CharField(max_length=10)
    marketprice1 = models.CharField(max_length=10)

    img2 = models.CharField(max_length=100)
    childcid2 = models.CharField(max_length=10)
    productid2 = models.CharField(max_length=10)
    longname2 = models.CharField(max_length=100)
    price2 = models.CharField(max_length=10)
    marketprice2 = models.CharField(max_length=10)

    img3 = models.CharField(max_length=100)
    childcid3 = models.CharField(max_length=10)
    productid3 = models.CharField(max_length=10)
    longname3 = models.CharField(max_length=100)
    price3 = models.CharField(max_length=10)
    marketprice3 = models.CharField(max_length=10)

    class Meta:
        db_table = 'axf_mainshow'



# insert into
# (typeid,typename,childtypenames,typesort)
# ("104749","热销榜","全部分类:0",1),
# ("104747","新品尝鲜","全部分类:0",2),
# ("103532","优选水果","全部分类:0#进口水果:103534#国产水果:103533",3)

# typeid 分类ID
# 进口水果:103534   》》》  子类名称:子类ID
class Foodtypes(models.Model):
    # 分类ID
    typeid = models.CharField(max_length=10)
    # 分类名称
    typename = models.CharField(max_length=100)
    # 子类列表  [包含有分类下 子类]
    childtypenames = models.CharField(max_length=256)
    # typesort 分类显示顺序
    typesort = models.IntegerField()

    class Meta:
        db_table = 'axf_foodtypes'


# 商品 模型类
# insert into
# axf_goods
# (productid,productimg,productname,productlongname,isxf,pmdesc,specifics,price,marketprice,categoryid,childcid,childcidname,dealerid,storenums,productnum)
# values
# ("11951","http://img01.bqstatic.com/upload/goods/000/001/1951/0000011951_63930.jpg@200w_200h_90Q","","乐吧薯片鲜虾味50.0g",0,0,"50g",2.00,2.500000,103541,103543,"膨化食品","4858",200,4);
class Goods(models.Model):
    # 商品ID
    productid = models.CharField(max_length=10)
    # 商品图片
    productimg = models.CharField(max_length=100)
    # 商品名称
    productname = models.CharField(max_length=100)
    # 商品长名称
    productlongname = models.CharField(max_length=200)
    # 是否精选
    isxf = models.IntegerField(default=0)
    # 是否买一送一
    pmdesc = models.IntegerField(default=0)
    # 规格
    specifics = models.CharField(max_length=100)
    # 价格
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # 超市价格
    marketprice = models.DecimalField(max_digits=8, decimal_places=2)
    # 分类ID
    categoryid = models.IntegerField()
    # 子类ID
    childcid = models.IntegerField()
    # 子类名称
    childcidname = models.CharField(max_length=100)
    # 详情ID
    dealerid = models.CharField(max_length=100)
    # 库存
    storenums = models.IntegerField()
    # 销量
    productnum = models.IntegerField()

    class Meta:
        db_table = 'axf_goods'


class User(models.Model):
    # 邮箱 【邮箱登录】
    email = models.CharField(max_length=20, unique=True)
    # 密码
    password = models.CharField(max_length=256)
    # 名字
    name = models.CharField(max_length=100)
    # 手机号
    phone = models.CharField(max_length=20)
    # 头像
    img = models.CharField(max_length=20, default='axf.png')
    # 等级
    rank = models.IntegerField(default=1)
    # 令牌
    token = models.CharField(max_length=256)

    class Meta:
        db_table = 'axf_user'


# 购物车 模型类
class Cart(models.Model):
    # 用户
    user = models.ForeignKey(User)

    # 商品
    goods = models.ForeignKey(Goods)

    # 额外信息 【手机: 版本、颜色、容量大小、数量...】
    # 商品数量
    number = models.IntegerField()
    # 是否选中
    isselect = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'


# 订单 模型类
# 一个用户 对应 多个订单
class Order(models.Model):
    # 用户
    user = models.ForeignKey(User)
    # 状态
    # -2 退款
    # -1 过期
    # 0 未付款
    # 1 已付款，未发货
    # 2 已付款，已发货
    # 3 已签收，未评价
    # 4 已评价
    status = models.IntegerField(default=0)
    # 创建时间
    createtime = models.DateTimeField(auto_now_add=True)
    # 订单号
    identifier = models.CharField(max_length=256)

    class Meta:
        db_table = 'axf_order'



# 订单商品 模型类
# 一个订单 对应 多个商品
class OrderGoods(models.Model):
    # 订单
    order = models.ForeignKey(Order)
    # 商品
    goods = models.ForeignKey(Goods)
    # 商品规格
    number = models.IntegerField()

    class Meta:
        db_table = 'axf_ordergoods'