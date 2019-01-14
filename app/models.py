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