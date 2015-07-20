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
jQuery('.mainMenuList li').bind('focusin mouseover', function() {

	jQuery(this).find('img').attr("src", jQuery(this).find('img').attr("src").replace("off.gif","r.gif"));
});
jQuery('.mainMenuList li').bind('focusout mouseout', function() {

	jQuery(this).find('img').attr("src", jQuery(this).find('img').attr("src").replace("r.gif","off.gif"));

});


jQuery('#uGnb li').click(function() {
	jQuery('#uGnb li').removeClass("hover");
	jQuery(this).addClass("hover");
});





function validateLogin(){
	var x = $('input[name="account"]').val();
	var y = $('input[name="password"]').val();
	if (x == null || x == ""){
		alert("아이디를 입력하세요.");
		return false;
	}
	else if(x.length <= 4 || x.length > 20){
		alert("아이디는 5~20자 이상입니다.");
		return false;
	}
	else{
		if (y == null || y == ""){
			alert("비밀번호를 입력하세요.");
			return false;
		}
		else if(y.length <= 3 || y.length > 20){
			alert("비밀번호는 4~20자 이상입니다.");
			return false;
		}
		else{
			return true;
		}
	}
}

function validateSignup(){
	var x = $('input[name="account"]').val();
	var y = $('input[name="password"]').val();
	var z = $('input[name="password_confirm"]').val();
	if (x == null || x == ""){
		alert("아이디를 입력하세요.");
		return false;
	}
	else if(x.length <= 4 || x.length > 20){
		alert("아이디는 5~20자 이상입니다.");
		return false;
	}
	else{
		if (isInt(x)){
			alert("아이디는 숫자로만 만들수 없습니다.");
			return false;
		}
		else{
			if (y == null || y == ""){
				alert("비밀번호를 입력하세요.");
				return false;
			}
			else if(y.length <= 3 || y.length > 20){
				alert("비밀번호는 4~20자 이상입니다.");
				return false;
			}
			else{
				if (y == z){
					var a = $('input[name="nickname"]').val();
					var b = $('input[name="phone"]').val();
					var c = $('input[name="bank"]').val();
					var d = $('input[name="bank_account"]').val();
					var e = $('input[name="bank_name"]').val();
					var f = $('input[name="rec_person"]').val();
					if(a==""||b==""||c==""||d==""||e==""||f==""){
						alert('입력되지 않은 값이 있습니다.');	
						return false;
					}
					else{
						return true;
					}
				}
				else{
					alert("두 비번이 다릅니다.");
					return false;
				}
			}

		}
	}
}


function isInt(x){
	var y = parseInt(x, 10);
	return !isNaN(y) && x == y && x.toString() == y.toString();
}
