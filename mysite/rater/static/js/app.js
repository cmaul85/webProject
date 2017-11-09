$(document).ready(function() {
	console.log( "ready!" );
	$("a").on("click", function(e){
		$(".active").removeClass('active');
		$(this).parent().addClass('active');
	
	});
});

