$(function () {
    $('.market').width(innerWidth)

    // 获取 分类下标，并设置对应的样式
    var typeIndex = $.cookie('typeIndex')
    if(typeIndex){  // 有值(之前有操作过)
        $('.type-item').eq(typeIndex).find('span').show()
    } else {    // 第一次进入
        $('.type-item:first').find('span').show()
    }
    
    
    // 侧边栏 点击
    $('.type-item').click(function () {
        // 记录下标
        /* jquery.cookie操作
            # 设置
            $.cookie(key, vlaue, options)
                options选项 {expires:过期时间, path: 路径}

            # 获取
            $.cookie(key)

            # 删除
            $.cookie(key, null)
        */
        $.cookie('typeIndex', $(this).index(), {path: '/'})
    })


    // 全部类型点击
    var categoryShow = false
    $('#category-bt').click(function () {
        console.log('全部类型点击')
            // 取反
            categoryShow = !categoryShow

            // 三目运算符
            categoryShow ? categoryViewShow() : categoryViewHide()
        }
    )

    // 综合排序点击
    var sortShow = false
    $('#sort-bt').click(function () {
        console.log('综合排序点击')
            // 取反
            sortShow = !sortShow

            // 三目运算符
            sortShow ? sortViewShow() : sortViewHide()
        }
    )
    
    // 蒙层点击
    $('.bounce-view').click(function () {
        sortShow = false
        sortViewHide()

        categoryShow = false
        categoryViewHide()
    })




    // 默认减和数字 隐藏 【存在问题】
    // $('.bt-wrapper .glyphicon-minus').hide()
    // $('.bt-wrapper .num').hide()

    // 如果number是有值，表示已经是有添加在购物车 【减号和数字就显示】
    $('.bt-wrapper .num').each(function () {
        var num = parseInt($(this).html())
        if (num){   // 显示
            $(this).prev().show()
            $(this).show()
        } else {    // 隐藏
            $(this).prev().hide()
            $(this).hide()
        }
    })


    // 商品加操作
    $('.bt-wrapper .glyphicon-plus').click(function () {
        // console.log('加操作')

        // 加入购物车: 谁、商品、加
        // 谁?  状态保持（必须登录）
        // 商品？   商品ID，添加一个自定义属性

        var goodsid = $(this).attr('goodsid')

        // 指向 点击的加按钮
        // console.log($(this).prev())

        // 保存当前点击按钮 【为了解决下面ajax后的操作】
        var $that = $(this)

        data = {
            'goodsid':goodsid
        }
        $.get('/axf/addcart/', data, function (response) {
            console.log(response)
            if (response.status == 0) { // 未登录
                window.open('/axf/login', target='_self')
            } else  if (response.status == 1) { // 加操作成功
                // 只能修改你所操作的 对应商品
                // 以下操作是所有的，是存在问题的!
                // 解决方案: this
                // $('.bt-wrapper .glyphicon-minus').show()
                // $('.bt-wrapper .num').show().html(response.number)

                // 注意: this 谁调用指向谁
                // $(this) ajax
                // 需要 指向 当前点击的按钮
                $that.prev().show().html(response.number)
                $that.prev().prev().show()
            }
        })
    })

    // 商品减操作
    $('.bt-wrapper .glyphicon-minus').click(function () {
        console.log('减操作')

        var goodsid = $(this).attr('goodsid')
        var $that = $(this)

        data = {
            'goodsid':goodsid
        }

        $.get('/axf/subcart/', data, function (response) {
            console.log(response)
            if (response.status == 1){  // 操作成功
                if (response.number > 0) {  // 改变个数
                    $that.next().html(response.number)
                } else {    // 隐藏减和个数
                    $that.next().hide()
                    $that.hide()
                }
            }
        })
    })


    function categoryViewShow() {
        sortShow = false
        sortViewHide()
        $('.category-view').show()
        $('#category-bt i').removeClass('glyphicon-triangle-top').addClass('glyphicon-triangle-bottom')
    }
    
    function categoryViewHide() {
        $('.category-view').hide()
        $('#category-bt i').removeClass('glyphicon-triangle-bottom').addClass('glyphicon-triangle-top')
    }

    function sortViewShow() {
        categoryShow = false
        categoryViewHide()
        $('.sort-view').show()
        $('#sort-bt i').removeClass('glyphicon-triangle-top').addClass('glyphicon-triangle-bottom')
    }

    function sortViewHide() {
        $('.sort-view').hide()
        $('#sort-bt i').removeClass('glyphicon-triangle-bottom').addClass('glyphicon-triangle-top')
    }
})