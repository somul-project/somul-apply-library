$(document).ready(function () {
  $(".paper").show();
  $(".spinner-preloader").hide();
});

function submit() {
  if (!validateEmail()) return false;
  if (!validatePhone()) return false;
  if (!validatePasswordCheck()) return false;
  // send
  
  var dict = {
      'name': $('#name').val(),
      'email': $('#email').val(),
      'phone': $('#phone').val(),
      'password': $('#password').val()
  };
  
  $.ajax({
      type: "PUT",
      url: "/api/v1/user",
      data: JSON.stringify(dict),
      error: function(err) {
          if (err.status == 400) {
              alert("오류가 발생하였습니다. 운영자에게 문의해주십시오.");
          }
      },
      beforeSend: function() {
          $(".paper").hide();
          $(".spinner-preloader").show();
      },
      success: function(data) {
          if (data.result == 0) {
              location.href = "/volunteer/information";
          } else {
              alert("오류가 발생하였습니다. 운영자에게 문의해주십시오.");
          }
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