$(function () {
    $('.login').width(innerWidth)


    // 邮箱验证
    $('#email input').blur(function () {
        var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/

        if(reg.test( $(this).val() )){  // 符合
            $('#email').removeClass('has-error').addClass('has-success')
            $('#email>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        } else {    // 不符合
            $('#email').removeClass('has-success').addClass('has-error')
            $('#email>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })

    // 密码验证
    $('#password input').blur(function () {
        var reg = /^[a-zA-Z\d_]{6}$/

        if (reg.test( $(this).val() )){  // 符合
            $('#password').removeClass('has-error').addClass('has-success')
            $('#password>span').removeClass('glyphicon-remove').addClass('glyphicon-ok')
        } else {    // 不符合
            $('#password').removeClass('has-success').addClass('has-error')
            $('#password>span').removeClass('glyphicon-ok').addClass('glyphicon-remove')
        }
    })


    // 触发登录
    $('#subButton').click(function () {
        var islogin = true

        // 遍历所有的输入框是否正确
        $('.form-group').each(function () {
            if ( !$(this).hasClass('has-success') ){
                islogin = false
            }
        })

        if (islogin){    // 都正确
            $('#login').submit()
        }
    })
})