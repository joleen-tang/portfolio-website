function toggleElementVisibility(elementId){
	$("#"+elementId).toggle("slow");
}

$(document).ready(function(){
	$(".collapsable-sub-heading").click(function(){
		$(this).siblings().slideToggle("slow");
		$(this).children("i").toggleClass("fa-caret-left");
	})
});