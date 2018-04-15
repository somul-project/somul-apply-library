// Validate

function validateEmail() {

    var email = document.getElementById("email");
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (!re.test(String(email.value.toLocaleLowerCase()))) {
        alert("잘못 된 이메일 형식입니다.");
        return false;
    }
    return true;
}

function validatePhone() {
    var input = document.querySelector('#phone');
    var re = /^(01[016789]{1}|02|0[3-9]{1}[0-9]{1})-?[0-9]{3,4}-?[0-9]{4}$/;
    if (!re.test(input.value)) {
        alert("핸드폰 번호 형식에 맞지 않습니다. 다시 입력해주세요.")
        window.scrollTo(0, window.scrollY + input.getBoundingClientRect().top - 60);
        $(input).effect("highlight", {color: '#F48FB1'}, 800);
        return false;
    }
    return true;
}

function validateNotEmpty() {
    var input = document.querySelectorAll('.input');
    var i = 0;
    if (input.length == 0) return true;
    for (i = 0; i < input.length; i++) {
        var trimed = input[i].value.trim();
        if (trimed.length == 0) {
            window.scrollTo(0, window.scrollY + input[i].getBoundingClientRect().top - 60);
            $(input[i]).effect("highlight", {color: '#F48FB1'}, 800);
            return false;
        }
    }    
    return true;
}

function validateDropDownChecked(dropDownList) {
    
    var i;
    for (i = 0; i < dropDownList.length; i++) {
        var id = dropDownList[i];
        var dropDownClicked = document.getElementById(id + "_isClicked");
        if (dropDownClicked.value !== "true") {
            window.location.hash = '';
            window.location.hash = '#' + id;
            window.scrollBy(0, -120);
            
            var child = document.querySelector('#' + id + ' .dropbtn');
            child.style.color = "red";
            return false;
        }
    }
    
    return true;
}

function validateRadio() {         
    var radio_check_val = "";

    if (document.getElementsByName('rule_radio').length == 0) return true;

    for (i = 0; i < document.getElementsByName('rule_radio').length; i++) {
        if (document.getElementsByName('rule_radio')[i].checked) {
            radio_check_val = document.getElementsByName('rule_radio')[i].value;
            return radio_check_val; 
        }        
    }

    if (radio_check_val === "")
    {
        window.location.hash = '';
        window.location.hash = '#rule_radio';
        window.scrollBy(0, -120);
        return false;
    }        
}

function validatePasswordCheck() {
    if (document.getElementById("password").value == document.getElementById("check_password").value) {
        return true;
    } else {
        alert("비밀번호와 비밀번호 확인의 값이 다릅니다.");
        return false;
    }
}

function validateCheckBox() {
    if (document.getElementById("check").checked) {
        return true;
    } else {
        $('#check-form').effect("bounce");
    }
}
