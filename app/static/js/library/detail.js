$(document).ready(function() {
    // jQuery selectors for UI
    var $loader = $("#loader");
    
    var $manager_phone_number = $("#phoneNumber");
    var $search_library = $("#searchLibrary");
    var $search_fail = $("#search-fail");
    
    var $library_name = $("#library-name");
    var $volunteer_list = $("#volunteer-list");
    var $speaker_list = $("#speaker-list");
    
    var $search_result = $("#search-result");
    var $library_detail = $("#library-detail");
    
    
    var $speaker_none = $("#speaker-none");
    var $speaker_wait = $("#speaker-wait");
    var $volunteer_none = $("#volunteer-none");
    
    // Search library event handler
    $search_library.click(function (event) {
        event.preventDefault();
        let pn = $manager_phone_number.val().replace(/-/, "");
        
        if (!isNumber(pn)) {
            alert("올바른 번호를 입력해주세요.");
            return;
        }
        
        $.ajax({
            type: "POST",
            url: "/api/v1/library/detail",
            data: JSON.stringify({"phone_number" : pn}),
            error: function(err) {
                $search_fail.css("display", "block");
            },
            beforeSend: function() {
                hideComment();
                showPreloader();
            },
            success: function(response) {                
                // Library
                $library_name.text(response["library"]["location_detail"]);
                $.each(response["library"], (key, value) => {
                    $library_detail.find('#' + key).find("td").text(value);
                });
                
                // Volunteer
                $volunteer_list.empty();
                if (response["volunteers"].length !== 0) {
                    response["volunteers"].forEach(volunteer => {
                        var card = '<div class="card">';
                        card += '<div class="card-body">';
                        card += '<h5 class="card-title">' + volunteer["name"] + '</h5>';
                        card += '<p class="card-text"> Email : ' + volunteer["email"] + '</p>';
                        card += '<p class="card-text"> Phone : ' + volunteer["phone"] + '</p>';
                        card += '</div>';
                        card += '</div>';
                        $volunteer_list.append(card);
                    });
                } else {
                    $volunteer_none.css("display", "block");
                }
                
                // Speaker
                var count = 0;
                $speaker_list.empty();
                if (response["speakers"].length !== 0) {
                    response["speakers"].forEach(speaker => {
                        if (!speaker["admin_approved"]) return true;

                        count++;

                        var card = '<div class="card">';
                        card += '<div class="card-body">';
                        card += '<h5 class="card-title">' + speaker["user"]["name"] + '</h5>';
                        card += '<p class="card-text"> Email : ' + speaker["user"]["email"] + '</p>';
                        card += '<p class="card-text"> Phone : ' + speaker["user"]["phone"] + '</p>';
                        card += '<p class="card-text"> Title : ' + speaker["title"] + '</p>';
                        card += '<p class="card-text"> Description : ' + speaker["description"] + '</p>';
                        card += '<p class="card-text"> Introduce : ' + speaker["introduce"] + '</p>';
                        card += '</div>';
                        card += '</div>';
                        $speaker_list.append(card);
                    });
                } else {
                    $speaker_none.css("display", "block");
                }

                if (response["speakers"].length !== count) {
                    $speaker_wait.css("display", "block");
                    $speaker_wait.text(response["speakers"].length - count + "명의 강연자가 심사 대기중입니다.");
                }
                
                $search_result.css("display", "block");
            },
            complete: () => {
                hidePreloader();
            },
            contentType: 'application/json; charset=UTF-8',
            dataType: "json"
        });
    });
    
    var showPreloader = () => {
        $loader.css("display", "block");
    }
    
    var hidePreloader = () => {
        $loader.fadeOut("slow");   
    }
    
    var isNumber = function(s) {
        s += ''; // 문자열로 변환
        s = s.replace(/^\s*|\s*$/g, ''); // 좌우 공백 제거
        if (s == '' || isNaN(s)) return false;
        return true;
    }
    
    var hideComment = () => {
        $search_fail.css("display", "none");
        $search_result.css("display", "none");
        $speaker_none.css("display", "none");
        $speaker_wait.css("display", "none");
        $volunteer_none.css("display", "none");
    }
});
