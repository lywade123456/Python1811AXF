$(function () {
    // 为了保证屏幕宽度不受到影响
    $('.home').width(innerWidth)

    var topSwiper = new Swiper('#topSwiper', {
        pagination: '.swiper-pagination',
        slidesPerView: 1,
        paginationClickable: true,
        spaceBetween: 30,
        loop: true,
        autoplay: 3000,

        effect: 'coverflow',
        grabCursor: true,
        coverflow: {
            shadow: true,
            slideShadows: true,
            shadowOffset: 20,
            shadowScale: 0.94
        }
    });


    var mustbuySwiper = new Swiper('#mustbuySwiper', {
        paginationClickable: true,
        spaceBetween: 3,
        loop: true,
        autoplay: 3000,
        slidesPerView: 3,
        freeMode: true
    });

})