function libraryInfoModal(id) {
    $.ajax({
        type: "GET",
        url: "/api/v1/library/" + id,
        success: function(data) {
            console.log(data);
            Object.keys(data).forEach(function (value, index, array) {
                var val = data[value];
                if (value.search("fac_other") != -1 || value.search("req_speaker") != -1) {
                    if (val == "") val = "없음";
                } else if (value.search("fac_") != -1) {
                    val = val ? "제공 가능" : "제공 불가"; 
                }
                $("#modal-library-factor-" + value).html(val);
            });
            $("#modal-library").modal();
        },
        error: function(err) {
            alert("서버에 장애가 발생하였습니다.\n잠시 후에 다시 시도하시거나 운영진에게 문의해주세요.");
        },
        beforeSend: function() {
            $(".spinner-preloader").show();
        },
        complete : function() {
            $(".spinner-preloader").fadeOut("slow");   
        },
        contentType: 'application/json; charset=UTF-8',
        dataType: "json"
    });
}

function sendSpeakerRequest(id, time) {
    $("#modal-speaker").modal();
    $("#speaker-run").attr("onclick", "runSpeakerRequest(" + id + ", '" + time + "');");
}

function sendVolunteerRequest(id, time) {
    $("#modal-volunteer").modal();
    $("#volunteer-run").attr("onclick", "runVolunteerRequest(" + id + ");");
}

function runSpeakerRequest(id, time) {
    $.ajax({
        type: "GET",
        url: "/api/v1/match/speaker/" + id + "?time=" + time,
        error: function(err) {
            alert("서버에 장애가 발생하였습니다.\n잠시 후에 다시 시도하시거나 운영진에게 직접 접수해주세요.");
        },
        beforeSend: function() {
            $(".paper").hide();
            $(".spinner-preloader").show();
        },
        success: function(data) {
            if (data.result == 0) {
                alert("매칭 신청에 성공하였습니다.");
                location.href = "/volunteer/information";
            } else if (data.result == 1) {
                alert("이미 할당된 세션입니다. 다른 세션을 선택해주세요.");
                location.reload();
            } else {
                alert("서버에 장애가 발생하였습니다.\n잠시 후에 다시 시도하시거나 운영진에게 직접 접수해주세요.")
                location.reload();
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

function runVolunteerRequest(id) {
  $.ajax({
    type: "GET",
    url: "/api/v1/match/volunteer/" + id,
    error: function(err) {
        alert("서버에 장애가 발생하였습니다.\n잠시 후에 다시 시도하시거나 운영진에게 직접 접수해주세요.");
    },
    beforeSend: function() {
        $(".paper").hide();
        $(".spinner-preloader").show();
    },
    success: function(data) {
        if (data.result == 0) {
            alert("매칭 신청에 성공하였습니다.");
            location.href = "/volunteer/information";
        } else if (data.result == 1) {
            alert("이미 정원이 꽉 찼습니다. 다른 세션을 선택해주세요.");
            location.reload();
        } else {
            alert("서버에 장애가 발생하였습니다.\n잠시 후에 다시 시도하시거나 운영진에게 직접 접수해주세요.")
            location.reload();
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