$(document).ready(function () {
    $("#div1").hide();
});

$(document).on("click", "#btn1", function(event) {
	$("#div2").hide();
	$("#div1").show();
});

$(document).on("click", "#btn2", function(event) {
	$("#div1").hide();
	$("#div2").show();
});
