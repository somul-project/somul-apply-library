$(document).ready(function() {
    // jQuery selectors for UI
    var $manager_phone_number = $("#phoneNumber");
    var $search_library = $("#searchLibrary");

    var $library_name = $("#library-name");
    var $volunteer_list = $("#volunteer-list");
    var $search_result = $("#search-result");
    var $library_detail = $("#library-detail").find('tr');
    
    // Search library event handler
    $search_library.click(function (event) {
        event.preventDefault();
        let pn = $manager_phone_number.val().replace(/-/, "");

        if (!isNumber(pn)) {
            alert("올바른 번호를 입력해주세요.");
            return;
        }

        console.log($library_detail);

        // Library name
        $library_name.text(data["name"]);
        data["volunteers"].forEach(volunteer => {
            var card = '<div class="card">';
            card += '<div class="card-body">';
            card += '<h5 class="card-title">' + volunteer["name"] + ' ('+ volunteer["type"] +')</h5>';
            card += '<p class="card-text">r</p>';
            card += '</div>';
            card += '</div>';

            $volunteer_list.append(card);
        });

        $search_result.css("display", "block");
    });

    var isNumber = function(s) {
        s += ''; // 문자열로 변환
        s = s.replace(/^\s*|\s*$/g, ''); // 좌우 공백 제거
        if (s == '' || isNaN(s)) return false;
        return true;
    }
});
