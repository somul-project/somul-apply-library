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
    
    // Search library event handler
    $search_library.click(function (event) {
        event.preventDefault();
        let pn = $manager_phone_number.val().replace(/-/, "");
        
        if (!isNumber(pn)) {
            alert("올바른 번호를 입력해주세요.");
            return;
        }
        
        $.ajax({
            type: "GET",
            url: "/api/v1/library/detail/" + pn,
            error: function(err) {
                $search_fail.css("display", "block");
            },
            beforeSend: function() {
                $search_fail.css("display", "none");
                $search_result.css("display", "none");
                showPreloader();
            },
            success: function(response) {                
                // Library name
                $library_name.text(response["library"]["location_detail"]);
                $.each(response["library"], (key, value) => {
                    $library_detail.find('#' + key).find("td").text(value);
                });
                
                $volunteer_list.empty();
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
                
                $speaker_list.empty();
                response["speakers"].forEach(speaker => {
                    var card = '<div class="card">';
                    card += '<div class="card-body">';
                    card += '<h5 class="card-title">' + speaker["name"] + '</h5>';
                    card += '<p class="card-text"> Email : ' + speaker["email"] + '</p>';
                    card += '<p class="card-text"> Phone : ' + speaker["phone"] + '</p>';
                    card += '</div>';
                    card += '</div>';
                    $speaker_list.append(card);
                });
                
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
});
