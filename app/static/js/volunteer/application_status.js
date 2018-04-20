
$(document).ready(function () {
    $(".paper").show();
    $(".spinner-preloader").hide();
});


$("#submit").click(function (event) {
    event.preventDefault();
    if(!validateNotEmpty()) return false;
    if(!validateEmail()) return false;

    // $(".spinner-preloader").fadeOut("slow", function () {
    //     $(".paper").fadeIn("slow");
    // });
    
    var dict = {
        'email': $('#email').val(),
        'password': $('#password').val(),
    };
    
    $.ajax({
        type: "POST",
        url: "/api/v1/signin",
        data: JSON.stringify(dict),
        error: function(err) {
            if (err.status == 400) {
                alert("인증 정보가 잘못되었습니다. 다시 시도해주세요.");
            } else {
                alert("인증 처리 과정에서 오류가 발생했습니다. 운영자에게 문의해주세요.");
            }
            location.reload();
        },
        beforeSend: function() {
            $(".paper").hide();
            $(".spinner-preloader").show();
        },
        success: function(data) {
            location.href = "/volunteer/information";
        },
        contentType: 'application/json; charset=UTF-8',
        dataType: "json"
    });
});
