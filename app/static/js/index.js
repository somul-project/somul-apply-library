$(document).ready(function() {
  // jQuery selectors for input
  var $name = $("#name");
  var $roadAddress = $("#roadAddress");
  var $numberAddress = $("#numberAddress");
  var $detailAddress = $("#detailAddress");
  var $managerName = $("#managerName");
  var $managerEmail = $("#managerEmail");
  var $managerPhone = $("#managerPhone");
  var $capacity = $("#capacity");
  var $facilityBeamOrScreen = $("#facilityBeamOrScreen");
  var $facilitySound = $("#facilitySound");
  var $facilityRecord = $("#facilityRecord");
  var $facilityPlacard = $("#facilityPlacard");
  var $facilitySelfPromo = $("#facilitySelfPromo");
  var $facilityOther = $("#facilityOther");
  var $requirements = $("#requirements");

  // jQuery selectors for validation
  var $infoHoldValid = $("#infoHoldValid");
  var $insufficientValid = $("#insufficientValid");

  // jQuery selectors for UI
  var $search_postcode = $("#searchPostcode");
  var $submit = $("#submit");

  // Daum Postcode API
  var postcode = new daum.Postcode({
    oncomplete: function(data) {
      // 도로명 주소의 노출 규칙에 따라 주소를 조합한다.
      // 내려오는 변수가 값이 없는 경우엔 공백('') 값을 가진다.
      var fullRoadAddr = data.roadAddress; 
      var extraRoadAddr = '';

      // 법정동명이 있을 경우 추가한다. (법정리는 제외)
      // 법정동의 경우 마지막 문자가 동, 로, 혹은 가로 끝난다.
      if (data.bname !== '' && /[동|로|가]$/g.test(data.bname)){
          extraRoadAddr += data.bname;
      }
      // 건물명이 있고, 공동 주택일 경우 추가한다.
      if (data.buildingName !== '' && data.apartment === 'Y'){
          extraRoadAddr += (extraRoadAddr !== '' ? ', ' + data.buildingName : data.buildingName);
      }
      // 도로명, 지번 조합형 주소가 있을 경우, 괄호까지 추가한 최종 문자열을 만든다.
      if (extraRoadAddr !== ''){
          extraRoadAddr = ' (' + extraRoadAddr + ')';
      }
      // 도로명, 지번 주소의 유무에 따라 해당 조합형 주소를 추가한다.
      if (fullRoadAddr !== ''){
          fullRoadAddr += extraRoadAddr;
      }

      // 우편번호와 주소 정보를 해당 필드에 넣는다.
      $roadAddress.val(fullRoadAddr + " (" + data.zonecode + ") ");
      $numberAddress.val(data.jibunAddress);
    }
  });

  // Postcode event handler
  $search_postcode.click(function (event) {
    event.preventDefault();
    postcode.open();
  });

  // Submit event handler
  $submit.click(function (event) {
    event.preventDefault();

    // 필수 동의 항목 값 확인
    if (
      !($infoHoldValid.is(':checked')) || 
      !($insufficientValid.is(':checked'))
    ) {
        alert("최하단 필수 동의 항목에 동의해주셔야 합니다.");
        return;
    }
  
    // 필수 작성 항목 값 확인
    if ($name.val() == "") {
      alert("도서관 이름을 적어주십시오.");
      return;
    }

    if ($roadAddress.val() == "" && $numberAddress.val() == "") {
      alert("도서관 소재지 주소를 검색해주십시오.");
      return;
    }

    if ($managerName.val() == "") {
      alert("담당자 이름을 적어주십시오.");
      return;
    }

    if ($managerEmail.val() == "") {
      alert("담당자 E-mail을 적어주십시오.");
      return;
    }
    
    if ($managerPhone.val() == "") {
      alert("담당자 전화번호를 적어주십시오.");
      return;
    }

    if ($capacity.val() == "") {
      alert("수용 가능 청중 규모를 적어주십시오.");
      return;
    }

    // Payload build-up
    payload = {
      name: $name.val(),
      roadAddress: $roadAddress.val(),
      numberAddress: $numberAddress.val(),
      detailAddress: $detailAddress.val(),
      managerName: $managerName.val(),
      managerEmail: $managerEmail.val(),
      managerPhone: $managerPhone.val(),
      capacity: $capacity.val(),
      facilityBeamOrScreen: $facilityBeamOrScreen.is(':checked'),
      facilitySound: $facilitySound.is(":checked"),
      facilityRecord: $facilityRecord.is(":checked"),
      facilityPlacard: $facilityPlacard.is(":checked"),
      facilitySelfPromo: $facilitySelfPromo.is(":checked"),
      facilityOther: $facilityOther.val(),
      requirements: $requirements.val()
    }

    // Request
    $.ajax({
        type: "POST",
        url: '/api/v1/apply',
        dataType: 'json',
        async: false,
        data: JSON.stringify(payload),
        contentType: 'application/json',
        success: function (data) {
          if (data.result == 0) location.href = "/success";
          else location.href = "/failure";
        }
    });
  });
});