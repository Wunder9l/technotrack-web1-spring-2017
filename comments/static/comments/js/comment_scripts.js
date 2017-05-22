/**
 * Created by artem on 19.04.17.
 */
var AUTOUPDATABLE_INTERVAL = 5000 // in milliseconds
$(document).ready(
    function () {
        window.setInterval(
            function () {
                $('.autoupdatable').each(function () {
                    // alert($(this).name)
                    $(this).load($(this).data('url'));
                })
            },
            // 1000
            AUTOUPDATABLE_INTERVAL
        )
    }
)

// function () {
    //     $('.autoupdatable').each(function () {
    //         // alert($(this).data('url'))
    //         $(this).load($(this).data('url'));
    //     })
    // }