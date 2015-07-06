$(document).ready(function(){
	// 경기 추가
	$('#sport').change(function(){
		$.ajax({
			url : '/admin/league',
			type: 'POST',
			dataType: 'json',
			data: { 
				sport : $(this).val()
			},
			success : function(resp){
				var league = document.getElementById('league');
				league.remove(league.selectedIndex)
				var op = document.createElement("option");
				op.text = resp.msg;
				op.value = 'MU';
				league.add(op)
			},
			error : function(resp){
				console.log('error');
			}	
		});
		
	});
	$('#addgame').click(function(){
		$.ajax({
			url : '/admin/addgame',
			type: 'POST',
			dataType: 'json',
			data: { 
				date : $('input[name="date"]').val(),
				sport : $('select[name="sport"]').val(),
				league : $('select[name="league"]').val(),
				home : $('input[name="home"]').val(),
				away : $('input[name="away"]').val(),
			},
			success : function(resp){
				//ajax 니까...새로고침 말고 새로 추가된 것들만 추가하자
				//date = date.replace(/T/g," ");
				$('#gamelist').prepend(
					'<tr class="" id="'+resp.id +'"> <td></td><td>'+ resp.sport +'</td><td></td><td>'+ resp.home +'</td><td></td><td>'+resp.away+'</td><td></td><td></td>');	
			},
			error : function(resp){
				console.log('error');
			}	
		});
	});
});
