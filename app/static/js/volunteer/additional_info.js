
$(document).ready(function () {
  $(".paper").show();
  $(".spinner-preloader").hide();
});

function submit() {
  var dict = {
      'introduce': $('#introduce').val(),
      'history': $('#history').val(),
      'title': $('#title').val(),
      'description': $('#description').val(),
      'keynote_link': $('#keynote_link').val(),
      'session_time': null
  };
  
  $.ajax({
      type: "POST",
      url: "/api/v1/speaker",
      data: JSON.stringify(dict),
      error: function(err) {
          alert("오류가 발생하였습니다. 운영자에게 문의하십시오.");
      },
      beforeSend: function() {
          $(".paper").hide();
          $(".spinner-preloader").show();
      },
      success: function(data) {
          alert("정상적으로 수정하였습니다.");
          location.href = "/volunteer/information";
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