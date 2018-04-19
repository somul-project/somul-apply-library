/* 
createWrapper([
    createTitleText("소프트웨어에<br>물들다<br>참여신청")
]);

createWrapper([
    createHr()
]);

createWrapper([
    createSubTitleText("개인정보 입력")
]);

createWrapper([
    createRadio(["강연자", "봉사자"])
]);

createWrapper([
    createPlaneText("이름"),
    createInput("text", null, "이름을 입력해 주세요.")
]);

createWrapper([
    createPlaneText("이메일"),
    createInput("email", "email", "이메일을 입력해 주세요."),
    createButton("blue", "인증번호 보내기", "sendConfirmMail()")
]);

createWrapper([
    createPlaneText("인증번호"),
    createInput("text", null, "인증번호를 입력해주세요")
]);

createWrapper([
    createPlaneText("휴대폰 번호"),
    createInput("text", "phone", "휴대폰 번호를 입력해 주세요.")
]);

createWrapper([
    createPlaneText("비밀번호 설정"),
    createInput("password", "password", "비밀번호를 입력해 주세요."),
    createInput("password", "check_password","재입력 해주세요")
]);

createWrapper([
    createPlaneText("개인정보 수집"),
    createCheckBox("동의"),
]);

createWrapper([
    createButton("yellow", "완료", "submit()")
]);

// Functions

function sendConfirmMail() {
    // validate
    if (!validateEmail()) return false;
    // send
    // 살려줘요 TODO AM 02:46
    
}
*/

$(document).ready(function () {
    $(".paper").show();
    $(".spinner-preloader").hide();
});

function submit() {
    if (!validateNotEmpty()) return false;
    if (!validateEmail()) return false;
    if (!validatePhone()) return false;
    if (!validatePasswordCheck()) return false;
    if (!validateCheckBox()) return false;
    
    // send
    
    var dict = {
        'name': $('#name').val(),
        'email': $('#email').val(),
        'phone': $('#phone').val(),
        'password': $('#password').val(),
        'has_experienced_somul': $('#option1').hasClass('active'),
    };
    
    $.ajax({
        type: "POST",
        url: "/api/v1/user",
        data: JSON.stringify(dict),
        error: function(err) {
            alert("오류가 발생하였습니다. 다시 시도해주십시오.");
            $("#application-submit").attr("disabled", false);
            $("#application-submit").html("완료");
        },
        beforeSend: function() {
            $("#application-submit").attr("disabled", true);
            $("#application-submit").html("요청 중입니다...");
            $(".paper").hide();
            $(".spinner-preloader").show();
        },
        success: function(data) {
            location.href = "/volunteer/success";
        },
        complete : function() {
            $(".spinner-preloader").fadeOut("slow", function () {
                $(".paper").fadeIn("slow");
            });   
        },
        contentType: 'application/json; charset=UTF-8',
        dataType: "json"
    });
}