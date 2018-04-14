$(document).ready(function () {
  $(".collapse-handler").click(function (e) {
    e.preventDefault();
    var id = $(this).attr("data-handle");
    $("#" + id).collapse("toggle");
  });
});