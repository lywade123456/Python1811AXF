$(function () {
    $('.cart').width(innerWidth)


    // 选择
    $('.cart .confirm-wrapper').click(function () {
        // 谁， 购物车（哪条记录）
        var cartid = $(this).attr('cartid')
        var $span = $(this).find('span')

        data = {
            'cartid':cartid
        }

        // 发起ajax
        $.get('/axf/changecartstatus/', data, function (response) {
            console.log(response)
            if (response.status){
                if (response.isselect){ // 选中
                    $span.removeClass('no').addClass('glyphicon glyphicon-ok')
                } else {    // 未选中
                    $span.removeClass('glyphicon glyphicon-ok').addClass('no')
                }
            }
        })
    })
    
    // 全选操作
    $('.bill .all').click(function () {
        // 获取
        var isall = $(this).attr('isall')
        // 转换
        isall = (isall=='true') ? true : false
        // 取反
        isall = !isall
        // 设置回去
        $(this).attr('isall', isall)

        if (isall){
            $(this).find('span').removeClass('no').addClass('glyphicon glyphicon-ok')
        } else {
            $(this).find('span').removeClass('glyphicon glyphicon-ok').addClass('no')
        }

        // true/false
        data = {
            'isall':isall
        }

        $.get('/axf/changecartall/', data, function (response) {
            console.log(response)
            if (response.status == 1){
                $('.confirm-wrapper').each(function () {
                    if (isall){ // 选中
                        $(this).find('span').removeClass('no').addClass('glyphicon glyphicon-ok')
                    } else {    // 取消选中
                        $(this).find('span').removeClass('glyphicon glyphicon-ok').addClass('no')
                    }
                })
            }
        })
    })
})