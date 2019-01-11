$(function () {
    // 320px:  1rem >> 16px
    // 400px:  1rem >> ?

    document.documentElement.style.fontSize = innerWidth / 320 * 16 + 'px'
    // console.log(document.documentElement.style.fontSize)
})