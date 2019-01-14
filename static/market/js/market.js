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