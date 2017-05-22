/**
 * Created by artem on 5/15/17.
 */
$(document).ready(
    function () {
        $(document).on('submit', '.ajaxnewsform', function () {
            // alert($(this).data('url'));
            var form = this
            $.post(
                $(form).data('url'),
                $(form).serialize()
            ).done(function (data, status, response) {
                if (status == "success") {
                    // alert('Да вы знаток!');
                    location.reload();
                } else {
                    // нужно отобразить форму с ошибками
                    $(form).load(response)
                    alert('А вот и неправильно!'); // любое значение, кроме 2011
                }
                console.log(data, "====================\n", status, "====================\n", response)
            });
            return false;
        })
    }
)
