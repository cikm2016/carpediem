jQuery(function() {

	jQuery('#gnb li').bind('focusin mouseover', function() {
			jQuery(this).find('>ul').removeClass("hiddenX");
			jQuery(this).addClass("hover");
		});
		jQuery('#gnb li').bind('focusout mouseout', function() {
			jQuery(this).find('>ul').addClass("hiddenX");
			jQuery(this).removeClass("hover");
	});

	
   });




