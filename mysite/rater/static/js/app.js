$(document).ready(function() {
	$("a").on("click", function(e){
		$(".active").removeClass('active');
		$(this).parent().addClass('active');
	
	});
});

