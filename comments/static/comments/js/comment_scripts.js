/**
 * Created by artem on 19.04.17.
 */
$(document).ready(
    function () {
        $('.comments_list_autoupdate').each(function () {
            $(this).load($(this).data('url'));
        })
    }
)

