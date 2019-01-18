$(function () {
    $('.cart').width(innerWidth)

    total()

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

                total()
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

                total()
            }
        })
    })
    
    
    // 计算总数
    function total(){
        var sum = 0

        $('.goods').each(function () {
            var $confirm = $(this).find('.confirm-wrapper')
            var $content = $(this).find('.content-wrapper')

            // 选中
            if ($confirm.find('.glyphicon-ok').length){
                var num = $content.find('.num').attr('num')
                var price = $content.find('.price').attr('price')

                sum += num * price
            }
        })

        // 设置显示
        $('.bill .total').html(parseInt(sum))
    }
    
    
    
    // 下单
    $('#generateorder').click(function () {
        $.get('/axf/generateorder/', function (response) {
            console.log(response)
            if (response.status == 1){  // 订单详情页
                window.open('/axf/orderdetail/' + response.identifier + '/', target='_self')
            }
        })
    })
})