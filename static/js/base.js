$(document).ready(function(){
	// 유저 가입 승인, 거절
	$('.allow').click(function(){
		var id = $(this).closest('tr').attr('id');
		var check = confirm('가입 승인 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/user/allow',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					allow : 1
				},
				success : function(resp){
					if(resp.success){
						alert('가입 승인하였습니다.');
						$('#'+id).remove();	
					}
					else{
						alert('잘못된 아이디값입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.deallow').click(function(){
		var id = $(this).closest('tr').attr('id');
		var check = confirm('가입 거절 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/user/allow',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					allow : 0
				},
				success : function(resp){
					if(resp.success){
						alert('가입 거절하였습니다.');
						$('#'+id).remove();	
					}
					else{
						alert('잘못된 아이디값입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	/* 유저가 자기 정보 수정 */
	$('.pincode_modify').click(function(){
		var id = $(this).closest('tr').attr('id');
		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/pincode/modify',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					pincode : $("input[name='pincode_"+id+"']").val()
				},
				success : function(resp){
					if(resp.success){
						alert('수정 되었습니다.');
						$('#name_'+id).text(resp.name);
					}
					else{
						alert('잘못된 아이디값입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.pincode_users').click(function(){
		var id = $(this).closest('tr').attr('id');
		popupOpen('/admin/pincode/users/'+id, 'width=800, height=1000, resizable=yes,scrollbars=yes;');
	});
	$('.chk_login').click(function(){
		var id = $(this).closest('tr').attr('id');
		popupOpen('/admin/user/loginlog/'+id, 'width=800, height=1000, resizable=yes,scrollbars=yes;');
	});
	$('.detail').click(function(){
		var id = $(this).closest('tr').attr('id');
		popupOpen('/admin/user/detail/'+id, 'width=1000, height=800, resizable=yes,scrollbars=yes;');
	});
	$('.message_open').click(function(){
		var id = $('input[name="id"]').val();
		popupOpen('/admin/user/message/'+id, 'width=350, height=300, resizable=no,scrollbars=no;');
	});

	$('.popclose').click(function(){
		window.close();
	});
	$('.reload').click(function(){
		location.reload();
	});
	$('.view_bet').click(function(){
		var id = $('input[name="id"]').val();
		popupOpen('/admin/user/view/bet/'+id, 'width=1000, height=800, resizable=no,scrollbars=yes;');

	})
	$('.view_charge').click(function(){
		var id = $('input[name="id"]').val();
		popupOpen('/admin/user/view/charge/'+id, 'width=1000, height=800, resizable=no,scrollbars=yes;');

	})
	$('.view_exchange').click(function(){
		var id = $('input[name="id"]').val();
		popupOpen('/admin/user/view/exchange/'+id, 'width=1000, height=800, resizable=no,scrollbars=yes;');

	})
	/* 관리자가 유저 정보 수정 */
	$('.user_modify').click(function(){
		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/user/modify',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : $('input[name="id"]').val(),
					bank : $("#bank").val(),
					bank_account : $('#bank_account').val(),
					bank_name : $("#bank_name").val(),
					level : $("#level").val(),
					state : $('#state').val(),
					danger : $("#danger").val()
				},
				success : function(resp){
					if(resp.success){
						alert('수정 되었습니다.');
						location.reload();
					}
					else{
						alert('잘못된 아이디값입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.message_send').click(function(){
		var check = confirm('쪽지를 보내시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/user/send',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : $('input[name="id"]').val(),
					message : $('#message').val()
				},
				success : function(resp){
					if(resp.success){
						alert('전송완료');
						window.close();
					}
					else{
						alert('잘못된 아이디값입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('#blockip').click(function(){
		var ip = $('input[id="ip1"]').val();
		
		if (ip){
			var check = confirm('차단 하시겠습니까?');
			if (check){
				$.ajax({
					url : '/admin/user/blockip',
					type: 'POST',
					dataType: 'json',
					data: { 
						ip : ip
					},
					success : function(resp){
						if(resp.success){
							alert('차단완료');
							$('#iplist').prepend('<tr><td>'+resp.date+'</td><td>'+resp.ip+'</td></tr>');
						}
						else{
							alert(resp.msg);
						}
					},
					error : function(resp){
						console.log('server error');
					}	
				});
			}
		}
		else{
			alert('아이피를 입력하세요.');
		}
	});

	// 리그 종목 수정, 삭제
	$('.sport_modify').click(function(){
		var id = $(this).closest('tr').attr('id');
		var name = $('input[name="sport_'+id+'"]').val();
		var sort = $('input[name="sort_'+id+'"]').val();
		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/sport/modify',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					name : name,
					sort : sort
				},
				success : function(resp){
					if(resp.success){
						alert('수정 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.sport_all_modify').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var id = $(this).closest('tr').attr('id');
			var name = $('input[name="sport_'+id+'"]').val();
			var sort = $('input[name="sort_'+id+'"]').val();
			data.push({id:id, name:name, sort:sort})
		});	

		var check = confirm('적용 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/sport/allmodify',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.sport_delete').click(function(){
		var id = $(this).closest('tr').attr('id');
		var check = confirm('삭제 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/sport/delete',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id
				},
				success : function(resp){
					if(resp.success){
						alert('삭제 되었습니다.');
						$('#'+id).remove();
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	// 리그 국가 수정, 삭제
	$('.nation_modify').click(function(){
		var id = $(this).closest('tr').attr('id');
		var name = $('input[name="nation_'+id+'"]').val();
		var sort = $('input[name="sort_'+id+'"]').val();
		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/nation/modify',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					name : name,
					sort : sort
				},
				success : function(resp){
					if(resp.success){
						alert('수정 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.nation_all_modify').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var id = $(this).closest('tr').attr('id');
			var name = $('input[name="nation_'+id+'"]').val();
			var sort = $('input[name="sort_'+id+'"]').val();
			data.push({id:id, name:name, sort:sort})
		});	

		var check = confirm('적용 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/nation/allmodify',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.nation_delete').click(function(){
		var id = $(this).closest('tr').attr('id');
		var check = confirm('삭제 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/nation/delete',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id
				},
				success : function(resp){
					if(resp.success){
						alert('삭제 되었습니다.');
						$('#'+id).remove();
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.sp_na_deleteall').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var id = $(this).closest('tr').attr('id');
			data.push({id:id})
		});	

		var check = confirm('삭제 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/nation/alldelete',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('삭제 되었습니다.');
						$("input:checkbox[name=select]:checked").each(function(){
							var id = $(this).closest('tr').attr('id');
							$('#'+id).remove();
						});	
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	// 리그 수정, 삭제
	$('.league_modify').click(function(){
		var id = $(this).closest('tr').attr('id');
		var name = $('input[name="league_'+id+'"]').val();
		var sort = $('input[name="sort_'+id+'"]').val();
		var state = $('select[name="state_'+id+'"]').val();

		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/league/modify',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					name : name,
					sort : sort,
					state : state
				},
				success : function(resp){
					if(resp.success){
						alert('수정 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.league_all_modify').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var id = $(this).closest('tr').attr('id');
			var name = $('input[name="league_'+id+'"]').val();
			var state = $('select[name="state_'+id+'"]').val();
			var sort = $('input[name="sort_'+id+'"]').val();
			data.push({id:id, name:name, sort:sort, state:state})
		});	

		var check = confirm('적용 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/league/allmodify',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.league_delete').click(function(){
		var id = $(this).closest('tr').attr('id');
		var check = confirm('삭제 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/league/delete',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id
				},
				success : function(resp){
					if(resp.success){
						alert('삭제 되었습니다.');
						$('#'+id).remove();
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.league_deleteall').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var id = $(this).closest('tr').attr('id');
			data.push({id:id})
		});	

		var check = confirm('삭제 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/league/alldelete',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('삭제 되었습니다.');
						$("input:checkbox[name=select]:checked").each(function(){
							var id = $(this).closest('tr').attr('id');
							$('#'+id).remove();
						});	
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('select[name="league"]').change(function(){
		var league_id = $(this).val();
		if (league_id == 0){
			$('#detail_table').empty();
		}
		else{
			$.ajax({
				url : '/admin/league/detail/list',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : league_id
				},
				success : function(resp){
					if(resp.success){
						var list = resp.list
						for(var i=0; i<list.length; i++){
							if (list[i].menu == 1){
var menu = '<option value="1" selected>승무패</option> <option value="2">핸디캡</option> <option value="3">스페셜</option>';
							}
							else if (list[i].menu == 2){
var menu = '<option value="1">승무패</option> <option value="2" selected>핸디캡</option> <option value="3">스페셜</option>';
							}
							else{
var menu = '<option value="1">승무패</option> <option value="2">핸디캡</option> <option value="3" selected>스페셜</option>';
							}
							if (list[i].game == 1){
var game = '<option value="1" selected>승무패</option> <option value="2">핸디캡</option> <option value="3">언더오버</option>';
						}
						else if (list[i].game == 2){
var game = '<option value="1">승무패</option> <option value="2" selected>핸디캡</option> <option value="3">언더오버</option>';
						}
						else{
var game = '<option value="1">승무패</option> <option value="2">핸디캡</option> <option value="3" selected>언더오버</option>';
							}
							var tr = '<tr class="select" id="'+list[i].id +'"> <td> <input type="checkbox" name="select"></td> <td style="text-align:left;">'+list[i].league + list[i].name +'</td> <td><input type="text" name="name_'+list[i].id+'" class="form-control" value="'+list[i].name +'"></td> <td><input type="text" name="home_'+list[i].id+'" class="form-control" value="'+list[i].home +'"></td> <td><input type="text" name="away_'+list[i].id+'" class="form-control" value="'+ list[i].away +'"></td> <td> <select class="form-control"  name="menu_'+list[i].id+'">'+menu+' </select> </td> <td> <select class="form-control"  name="game_'+list[i].id+'">'+game+' </select> </td> <td> <button class="btn sBtn detail_modify">수정</button>/<button class="btn sBtn greyBtn detail_delete">삭제</button> </td> </tr>';
							$('#detail_table').append(tr);
						}	
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	// 세부 리그 수정, 삭제
	$('#detail_table').on("click",".detail_modify",function(){
		var id = $(this).closest('tr').attr('id');

		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/detail/modify',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					name : $('input[name="name_'+id+'"]').val(),
					home : $('input[name="home_'+id+'"]').val(),
					away : $('input[name="away_'+id+'"]').val(),
					game : $('select[name="game_'+id+'"]').val(),
					menu : $('select[name="menu_'+id+'"]').val()
				},
				success : function(resp){
					if(resp.success){
						alert('수정 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.detail_all_modify').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var id = $(this).closest('tr').attr('id');
			var name = $('input[name="name_'+id+'"]').val();
			var home = $('input[name="home_'+id+'"]').val();
			var away = $('input[name="away_'+id+'"]').val();
			var menu = $('select[name="menu_'+id+'"]').val();
			var game = $('select[name="game_'+id+'"]').val();
			data.push({id:id, name:name, home:home, away:away, menu:menu, game:game})
		});	

		var check = confirm('적용 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/detail/allmodify',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.detail_deleteall').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var id = $(this).closest('tr').attr('id');
			data.push({id:id})
		});	

		var check = confirm('삭제 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/detail/alldelete',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				},
				success : function(resp){
					if(resp.success){
						alert('삭제 되었습니다.');
						$("input:checkbox[name=select]:checked").each(function(){
							var id = $(this).closest('tr').attr('id');
							$('#'+id).remove();
						});	
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('#detail_table').on("click",".detail_delete",function(){
		var id = $(this).closest('tr').attr('id');
		var check = confirm('삭제 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/detail/delete',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id
				},
				success : function(resp){
					if(resp.success){
						alert('삭제 되었습니다.');
						$('#'+id).remove();
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('#detail_add').click(function(){
		var l = $('select[name="league"]').val();
		var m = $('select[name="menu"]').val();
		var g = $('select[name="game"]').val();
		if (l == 0){
			alert('리그를 선택하세요.');
			return false;
		}
		if (m == 0 || g == 0){
			alert('메뉴와 게임종류를 선택하세요.');
			return false;
		}
		$.ajax({
			url : '/admin/league/detail',
			type: 'POST',
			dataType: 'json',
			data: { 
				league : $('select[name="league"]').val(),
				name : $('input[name="name"]').val(),
				home : $('input[name="home"]').val(),
				away : $('input[name="away"]').val(),
				menu : $('select[name="menu"]').val(),
				game : $('select[name="game"]').val()
			},
			success : function(resp){
				if(resp.success){
					if (parseInt(resp.menu) == 1){
						var menu = '<option value="1" selected>승무패</option> <option value="2">핸디캡</option> <option value="3">스페셜</option>';
					}
					else if (parseInt(resp.menu) == 2){
						var menu = '<option value="1">승무패</option> <option value="2" selected>핸디캡</option> <option value="3">스페셜</option>';
					}
					else{
						var menu = '<option value="1">승무패</option> <option value="2">핸디캡</option> <option value="3" selected>스페셜</option>';
					}
					if (parseInt(resp.game) == 1){
						var game = '<option value="1" selected>승무패</option> <option value="2">핸디캡</option> <option value="3">언더오버</option>';
					}
					else if (parseInt(resp.game) == 2){
						var game = '<option value="1">승무패</option> <option value="2" selected>핸디캡</option> <option value="3">언더오버</option>';
					}
					else{
						var game = '<option value="1">승무패</option> <option value="2">핸디캡</option> <option value="3" selected>언더오버</option>';
					}
					var tr = '<tr class="select" id="'+resp.id +'"> <td> <input type="checkbox" name="select"></td> <td style="text-align:left;">'+resp.league + resp.name +'</td> <td><input type="text" name="name_'+resp.id+'" class="form-control" value="'+resp.name +'"></td> <td><input type="text" name="home_'+resp.id+'" class="form-control" value="'+resp.home +'"></td> <td><input type="text" name="away_'+resp.id+'" class="form-control" value="'+ resp.away +'"></td> <td> <select class="form-control"  name="menu">'+menu+' </select> </td> <td> <select class="form-control"  name="game">'+game+' </select> </td> <td> <button class="btn sBtn detail_modify">수정</button>/<button class="btn sBtn greyBtn detail_delete">삭제</button> </td> </tr>';
					$('#detail_table').append(tr);
				}
				else{
					alert('잘못된 접근입니다.');
				}
			},
			error : function(resp){
				console.log('server error');
			}	
		});

	});
	$('input[name="date_start"]').val(moment().year()+'-'+(moment().month()+1)+'-');
	$('input[name="date_end"]').val(moment().year()+'-'+(moment().month()+1)+'-');
	$('#searchadjust').submit(function(){
		var date_start = $('input[name="date_start"]').val();
		var date_end = $('input[name="date_end"]').val();

		if (date_start == "" || date_end == ""){
			alert('경기날짜와 시간을 입력하세요.');
			return false;
		}	
		else if (!moment(date_start, 'YYYY-M-D', true).isValid()){
			alert('날짜, 시간 형식이 잘못되었습니다.');
			return false;
		}	
		else if (!moment(date_end, 'YYYY-M-D', true).isValid()){
			alert('날짜, 시간 형식이 잘못되었습니다.');
			return false;
		}	
		else{
			return true;
		}
		
	});

	$('input[name="date_first"]').val(moment().year()+'-'+(moment().month()+1)+'-');
	$('input[name="date"]').val(moment().year()+'-'+(moment().month()+1)+'-');
	$('#waitgamebtn').click(function(){
		var game = $('select[name="game"]').val();
		var i;
		var date_first = $('input[name="date_first"]').val();
		var date_second = $('input[name="date_second"]').val();
		var league_name = $('select[name="league"] option:selected').text();

		if (date_first == "" || date_second == ""){
			alert('경기날짜와 시간을 입력하세요.');
			return false;
		}	
		else if (!moment(date_first+' '+date_second, 'YYYY-M-D HH:mm', true).isValid()){
			alert('날짜, 시간 형식이 잘못되었습니다.');
			return false;
		}	
		else{
			$.ajax({
				url : '/admin/register/game/getdetail',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : $('select[name="league"] option:selected').val()
				},
				success : function(resp){
					var list = resp.list
					if(resp.success){
						for (var i = 0;i<list.length; i++){
							if (parseInt(list[i].menu) == 1){
								$('.odd').append('<li><input type="checkbox" name="checked" value="'+list[i].id+'" checked>'+list[i].league+' '+list[i].name+'</li>');
							}
							else if (parseInt(list[i].menu) == 2){
								$('.handi').append('<li><input type="checkbox" name="checked" value="'+list[i].id+'" checked>'+list[i].league+' '+list[i].name+'</li>');
							}
							else{
								$('.spe').append('<li><input type="checkbox" name="checked" value="'+list[i].id+'" checked>'+list[i].league+' '+list[i].name+'</li>');
							}
						}
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
			$('.addlist').empty();
			for (i=0;i<game;i++){
				var str = '<tr> <td><input type="text" class="form-control" name="date_first_'+i+'" value="'+date_first+'" disabled></td> <td><input type="text" class="form-control" name="date_second_'+i+'" value="'+date_second+'" disabled></td> <td><input type="text" class="form-control" name="league_'+i+'" value="'+league_name+'" disabled></td> <td><input type="text" class="form-control home" name="home_'+i+'"></td> <td><input type="text" class="form-control away" name="away_'+i+'"></td> </tr>'
				$('.addlist').append(str);	
			}		
		}
		
	});
	$('#emptygamebtn').click(function(){
		$('.addlist').empty();
	});
	
	// 등록 경기 수정
	$('.game_modify').click(function(){
		var id = $(this).closest('tr').attr('id');

		var check = confirm('적용하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/register/game/modify',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					home_rate : $('input[name="home_rate_'+id+'"]').val(),
					away_rate : $('input[name="away_rate_'+id+'"]').val(),
					draw_rate : $('input[name="draw_rate_'+id+'"]').val()
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.game_delete').click(function(){
		var id = $(this).closest('tr').attr('id');
		var check = confirm('삭제 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/register/game/delete',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id
				},
				success : function(resp){
					if(resp.success){
						alert('삭제 되었습니다.');
						$('#'+id).remove();
					}
					else{
						
						alert(resp.msg);
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.cross_deleteall').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			data.push({id:tmp_id})
		});	
		var check = confirm('삭제 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/register/cross/deleteall',
				type: 'POST',
				dataType: 'json',
				data: { 
					data: JSON.stringify(data)
				},
				success : function(resp){
					if(resp.success){
						alert('삭제 되었습니다.');
						$("input:checkbox[name=select]:checked").each(function(){
							var id = $(this).closest('tr').attr('id');
							$('#'+id).remove();
						});	
						
					}
					else{
						alert(resp.msg);
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.game_deleteall').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			data.push({id:tmp_id})
		});	
		var check = confirm('삭제 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/register/game/deleteall',
				type: 'POST',
				dataType: 'json',
				data: { 
					data: JSON.stringify(data)
				},
				success : function(resp){
					if(resp.success){
						alert('삭제 되었습니다.');
						$("input:checkbox[name=select]:checked").each(function(){
							var id = $(this).closest('tr').attr('id');
							$('#'+id).remove();
						});	
						
					}
					else{
						alert(resp.msg);
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.ip_deleteall').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			data.push({id:tmp_id})
		});	
		var check = confirm('삭제 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/user/ip/deleteall',
				type: 'POST',
				dataType: 'json',
				data: { 
					data: JSON.stringify(data)
				},
				success : function(resp){
					if(resp.success){
						alert('삭제 되었습니다.');
						$("input:checkbox[name=select]:checked").each(function(){
							var id = $(this).closest('tr').attr('id');
							$('#'+id).remove();
						});	
						
					}
					else{
						alert(resp.msg);
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.register_all_apply').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			var tmp_state = $('#'+tmp_id).find('select').val();
			var tmp_home= $('#'+tmp_id).find('input[name="home_rate_'+tmp_id+'"]').val();
			var tmp_draw= $('#'+tmp_id).find('input[name="draw_rate_'+tmp_id+'"]').val();
			var tmp_away= $('#'+tmp_id).find('input[name="away_rate_'+tmp_id+'"]').val();
			data.push({id:tmp_id, state:tmp_state, home:tmp_home, draw:tmp_draw, away:tmp_away})
		});	

		var check = confirm('적용 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/register/game/applyall',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.cross_apply').click(function(){
		var id = $(this).closest('tr').attr('id');

		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/register/cross/apply',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					state : $('select[name="state_'+id+'"]').val()
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.cross_all_apply').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			var tmp_state = $('#'+tmp_id).find('select').val();
			var tmp_home= $('#'+tmp_id).find('input[name="home_rate_'+tmp_id+'"]').val();
			var tmp_draw= $('#'+tmp_id).find('input[name="draw_rate_'+tmp_id+'"]').val();
			var tmp_away= $('#'+tmp_id).find('input[name="away_rate_'+tmp_id+'"]').val();
			data.push({id:tmp_id, state:tmp_state, home:tmp_home, draw:tmp_draw, away:tmp_away})
		});	

		var check = confirm('적용 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/register/cross/applyall',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.handicap_all_apply').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			var tmp_state = $('#'+tmp_id).find('select').val();
			var tmp_home= $('#'+tmp_id).find('input[name="home_rate_'+tmp_id+'"]').val();
			var tmp_draw= $('#'+tmp_id).find('input[name="draw_rate_'+tmp_id+'"]').val();
			var tmp_away= $('#'+tmp_id).find('input[name="away_rate_'+tmp_id+'"]').val();
			var tmp_handi= $('#'+tmp_id).find('input[name="handicap_'+tmp_id+'"]').val();
			data.push({id:tmp_id, state:tmp_state, home:tmp_home, draw:tmp_draw, away:tmp_away, handicap:tmp_handi})
		});	

		var check = confirm('적용 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/register/handicap/applyall',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.ladder_all_apply').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			var tmp_odd = $('#'+tmp_id).find('input[name="odd_rate_'+tmp_id+'"]').val();
			var tmp_even = $('#'+tmp_id).find('input[name="even_rate_'+tmp_id+'"]').val();
			data.push({id:tmp_id, odd:tmp_odd, even:tmp_even})
		});	

		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/register/ladder/applyall',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.ladder_detail_all_apply').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			var tmp_state = $('#'+tmp_id).find('select[name="state_'+tmp_id+'"]').val();
			data.push({id:tmp_id, state:tmp_state})
		});	

		var check = confirm('적용 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/register/ladder/detail/applyall',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.ladder_detail_all_finish').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			var tmp_win = $('#'+tmp_id).find('select[name="win_'+tmp_id+'"]').val();
			data.push({id:tmp_id, win:tmp_win})
		});	

		var check = confirm('적용 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/finish/ladder/detail/applyall',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	// 입금 계좌 관리
	$('.bank_modify').click(function(){
		var id = $(this).closest('tr').attr('id');

		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/bank/account/modify',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					bank : $('input[name="bank_'+id+'"]').val(),
					bank_account : $('input[name="bank_account_'+id+'"]').val(),
					bank_name : $('input[name="bank_name_'+id+'"]').val()
				},
				success : function(resp){
					if(resp.success){
						alert('수정 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.bank_modifyall').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			var tmp_bank = $('input[name="bank_'+tmp_id+'"]').val();
			var tmp_bank_account = $('input[name="bank_account_'+tmp_id+'"]').val();
			var tmp_bank_name = $('input[name="bank_name_'+tmp_id+'"]').val();
			data.push({id:tmp_id, bank:tmp_bank, bank_account:tmp_bank_account, bank_name:tmp_bank_name })
		});	

		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/bank/account/modifyall',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('적용 되었습니다.');
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	// 충전 개별 수락
	$('.charge_one').click(function(){
		var id = $(this).closest('tr').attr('id');

		var check = confirm('충전 수락하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/bank/charge/allow',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id
				},
				success : function(resp){
					if(resp.success){
						alert('충전 완료 되었습니다.');
						$('#'+id).remove();
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	// 선택 항목 전체 충전 수락
	$('.charge_all').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			data.push({ id:tmp_id })
		});	

		var check = confirm('선택 항목들을 충전 수락하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/bank/charge/allowall',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('모두 충전하였습니다.');
						$("input:checkbox[name=select]:checked").each(function(){
							var tmp_id = $(this).closest('tr').attr('id');
							$('#'+tmp_id).remove();
						});	
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	// 환전 개별 수락
	$('.exchange_one').click(function(){
		var id = $(this).closest('tr').attr('id');

		var check = confirm('환전하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/bank/exchange/allow',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id
				},
				success : function(resp){
					if(resp.success){
						alert('환전 완료 되었습니다.');
						$('#'+id).remove();
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	// 선택 항목 전체 환전 수락
	$('.exchange_all').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			data.push({ id:tmp_id })
		});	

		var check = confirm('선택 항목들을 환전하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/bank/exchange/allowall',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('모두 환전하였습니다.');
						$("input:checkbox[name=select]:checked").each(function(){
							var tmp_id = $(this).closest('tr').attr('id');
							$('#'+tmp_id).remove();
						});	
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	// 환전 거절
	$('.cancel_one').click(function(){
		var id = $(this).closest('tr').attr('id');

		var check = confirm('환전을 거절하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/bank/exchange/deallow',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id
				},
				success : function(resp){
					if(resp.success){
						alert('환전요청이 거절되었습니다.');
						$('#'+id).remove();
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	// 선택 항목 전체 환전 수락
	$('.cancel_all').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			data.push({ id:tmp_id })
		});	

		var check = confirm('선택 항목들을 환전 거절하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/bank/exchange/deallowall',
				type: 'POST',
				dataType: 'json',
				data: {
					data: JSON.stringify(data)
				
				},
				success : function(resp){
					if(resp.success){
						alert('모두 환전 거절하였습니다.');
						$("input:checkbox[name=select]:checked").each(function(){
							var tmp_id = $(this).closest('tr').attr('id');
							$('#'+tmp_id).remove();
						});	
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.start_all').click(function(){
		$('.select').each(function(){
			var id = $(this).attr('id');
			$(this).find('select[name="state_'+id+'"]').val(1);
		});
	});
	$('.end_all').click(function(){
		$('.select').each(function(){
			var id = $(this).attr('id');
			$(this).find('select[name="state_'+id+'"]').val(3);
		});
	});
	$('.select_all').click(function(){
		var flag = 0;
		var len = $('.select').length;
		$('.select').each(function(){
			if ($(this).hasClass('clicked')){
				flag += 1;
			}
		});
		$('.select').each(function(){
			if (flag == len){
				$(this).removeClass('clicked');
				$(this).find("input:checkbox").prop("checked",false);
			}
			else{
				$(this).addClass('clicked');
				$(this).find("input:checkbox").prop("checked",true);
			}
		});
	});
	$('.container').on("click", ".select",function(){
		var check = $(this).hasClass('clicked')
		
		if (check){
			$(this).find("input:checkbox").prop("checked",false);
			$(this).removeClass('clicked');
		}
		else{
			$(this).find("input:checkbox").prop("checked",true);
			$(this).addClass('clicked');
		}
	});
	$('.cross_finish').click(function(){
		var id = $(this).closest('tr').attr('id');

		var check = confirm('마감 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/finish/cross',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					home_score : $('input[name="home_score_'+id+'"]').val(),
					away_score : $('input[name="away_score_'+id+'"]').val()
				},
				success : function(resp){
					if(resp.success){
						alert('마감 되었습니다.');
						$('#'+id).remove();
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.cross_finish_all').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			var tmp_home = $('input[name="home_score_'+tmp_id+'"]').val();
			var tmp_away = $('input[name="away_score_'+tmp_id+'"]').val();
			data.push({ id:tmp_id, home_score:tmp_home, away_score:tmp_away  })
		});	
		var id = $(this).closest('tr').attr('id');

		var check = confirm('마감 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/finish/cross/all',
				type: 'POST',
				dataType: 'json',
				data: { 
					data: JSON.stringify(data)
				},
				success : function(resp){
					if(resp.success){
						alert('마감 되었습니다.');
						$("input:checkbox[name=select]:checked").each(function(){
							var tmp_id = $(this).closest('tr').attr('id');
							$('#'+tmp_id).remove();
						});	
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.handicap_finish_all').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			var tmp_home = $('input[name="home_score_'+tmp_id+'"]').val();
			var tmp_away = $('input[name="away_score_'+tmp_id+'"]').val();
			data.push({ id:tmp_id, home_score:tmp_home, away_score:tmp_away  })
		});	
		var id = $(this).closest('tr').attr('id');

		var check = confirm('마감 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/finish/handicap/all',
				type: 'POST',
				dataType: 'json',
				data: { 
					data: JSON.stringify(data)
				},
				success : function(resp){
					if(resp.success){
						alert('마감 되었습니다.');
						$("input:checkbox[name=select]:checked").each(function(){
							var tmp_id = $(this).closest('tr').attr('id');
							$('#'+tmp_id).remove();
						});	
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('.cross_restore').click(function(){
		var id = $(this).closest('tr').attr('id');

		var check = confirm('복원 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/finish/restore',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id
				},
				success : function(resp){
					if(resp.success){
						alert('복원 되었습니다.');
						$('#'+id).remove();
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('#max_btn').click(function(){
		var money = $('input[name="maxbet"]').val();
		var rate_cml = parseFloat($('#rate_cml').text());

		if ((money*rate_cml) > $('input[name="maxgain"]').val()){
			alert('현재 배팅에 최대 배팅금액을 설정할수 없습니다.');
		}
		else{
			$('#money_bet').val(numberWithCommas($('input[name="maxbet"]').val()));
			$('#money_cml').text(numberWithCommas(Math.round(rate_cml*$('input[name="maxbet"]').val())));
		}

	});
	$(".clickbox").hover(
		function(){
			$(this).css("border-color","red");
			$(this).css("cursor","pointer");
		},
		function(){ 
			$(this).css("border-color","black");
		}
	);

	$('.bet_table').on("click",".bet_cancel",function(){
		var id = $(this).closest('tr').attr('id').split("_")[1];

		var rate_cml = parseFloat($('#rate_cml').text());
		var money_bet = parseInt($('#money_bet').val().replace(/\,/g,''));
		var rate = parseFloat($('#'+id).find('.clicked').find('.rate').text());

		var ret_rate;
		/* 같은팀 재클릭 */
		if (rate_cml == rate){
			ret_rate = 0;
		}
		else{
			ret_rate = rate_cml/rate;
		}

		$('#bet_'+id).remove();
		$('input[name="'+id+'"]').remove();
		$('#'+id).find('.clicked').removeClass('clicked');

		$('#rate_cml').text(numberWithCommas(ret_rate.toFixed(2)));
		$('#money_cml').text(numberWithCommas(Math.round(ret_rate*money_bet)));
		
	});
	$(".clickbox").click(function(){
		//var id = $(this).closest('tr').attr('id');
		var id = $(this).closest('div').attr('id');
		var	home = $('#'+id).find('td.home').find('span.name').text();
		var	away = $('#'+id).find('td.away').find('span.name').text();

		var rate_cml = parseFloat($('#rate_cml').text());
		var money_bet = parseInt($('#money_bet').val().replace(/\,/g,''));

		var check = $(this).hasClass('clicked')
		var rate = parseFloat($(this).find('span.rate').text());
		var	team = $(this).find('span.name').text();
		if (team == ""){
			team = '무승부';
		}
		
		var ret_rate;
		/* 같은팀 재클릭 */
		if (check){
			if (rate_cml == rate){
				ret_rate = 0;
			}
			else{
				ret_rate = rate_cml/rate;
			}
			$('#bet_'+id).remove();
			$('input[name="'+id+'"]').remove();
			$(this).removeClass('clicked');
			$('#rate_cml').text(numberWithCommas(ret_rate.toFixed(2)));
			$('#money_cml').text(numberWithCommas(Math.round(ret_rate*money_bet)));
		}
		/* 새로운팀 클릭 */
		else{
			var clicked = $('#'+id).find('p.clicked')
			/* 클릭된 팀이 없을때 */
			if (clicked.text() == ""){
				if (rate_cml == 0){
					ret_rate = rate;
				}
				else{
					ret_rate = rate_cml*rate;
				}
				if(Math.round(ret_rate*money_bet) > $('input[name="maxgain"]').val()){
					alert('최대 당첨금을 넘습니다.');	
				} 
				else{
					$(this).addClass('clicked');
					
					var betteam;
					var isHome = $(this).hasClass('home');
					if (isHome){
						$('.bet_table').prepend('<input class="mybet" type="hidden" name="'+id+'" value="1">');
						betteam = '<tr id="bet_'+id+'"><td>'+rate+'</td><td><div class="selected">'+home+'</div><div>'+away+'</div></td><td><button class="btn sBtn bet_cancel">X</button></td></tr>';
					}
					else{
						var isAway = $(this).hasClass('away');
						if(isAway){
							$('.bet_table').prepend('<input class="mybet" type="hidden" name="'+id+'" value="-1">');
							betteam = '<tr id="bet_'+id+'"><td>'+rate+'</td><td><div>'+home+'</div><div class="selected">'+away+'</div></td><td><button class="btn sBtn bet_cancel">X</button></td></tr>';
						}
						else{
							$('.bet_table').prepend('<input class="mybet" type="hidden" name="'+id+'" value="0">');
							betteam = '<tr id="bet_'+id+'"><td>'+rate+'</td><td><div>'+home+'</div><div>'+away+'</div></td><td><button class="btn sBtn bet_cancel">X</button></td></tr>';
						}
					}
					$('.bet_table').prepend(betteam);
					$('#rate_cml').text(numberWithCommas(ret_rate.toFixed(2)));
					$('#money_cml').text(numberWithCommas(Math.round(ret_rate*money_bet)));
				}
			}
			/* 클릭된 팀이 있을때 */
			else{
				var sameline = parseFloat(clicked.find('span.rate').text());
				if (rate_cml == sameline){
					ret_rate = rate
				}
				else{
					ret_rate = ((rate_cml/sameline)*rate);
				}

				if(Math.round(ret_rate*money_bet) > $('input[name="maxgain"]').val()){
					alert('최대 당첨금을 넘습니다.');	
				} 
				else{
					clicked.removeClass('clicked');
					$(this).addClass('clicked');
					$('#bet_'+id).remove();

					$('input[name="'+id+'"]').remove();


					var betteam;
					var isHome = $(this).hasClass('home');
					// 승,무,패 어디 선택됐는지 판단
					if (isHome){
						$('.bet_table').prepend('<input class="mybet" type="hidden" name="'+id+'" value="1">');
						betteam = '<tr id="bet_'+id+'"><td>'+rate+'</td><td><div class="selected">'+home+'</div><div>'+away+'</div></td><td><button class="btn sBtn bet_cancel">X</button></td></tr>';
					}
					else{
						var isAway = $(this).hasClass('away');
						if(isAway){
							$('.bet_table').prepend('<input class="mybet" type="hidden" name="'+id+'" value="-1">');
							betteam = '<tr id="bet_'+id+'"><td>'+rate+'</td><td><div>'+home+'</div><div class="selected">'+away+'</div></td><td><button class="btn sBtn bet_cancel">X</button></td></tr>';
						}
						else{
							$('.bet_table').prepend('<input class="mybet" type="hidden" name="'+id+'" value="0">');
							betteam = '<tr id="bet_'+id+'"><td>'+rate+'</td><td><div>'+home+'</div><div>'+away+'</div></td><td><button onclick="bet_cancel()" class="btn sBtn bet_cancel">X</button></td></tr>';
						}
					}
					$('.bet_table').prepend(betteam);
					$('#rate_cml').text(numberWithCommas(ret_rate.toFixed(2)));
					$('#money_cml').text(numberWithCommas(Math.round(ret_rate*money_bet)));
				}

			}
		}
	});
	//승무패 배팅
	$('#crossbet_btn').click(function(){
		var money_crt = parseInt($('#money_crt').text().replace(/\,/g,''));
		var money_bet = parseInt($('#money_bet').val().replace(/\,/g,''));
		var rate = $('#rate_cml').text();
		if (money_bet > money_crt){
			alert('캐쉬가 부족합니다.');
		}
		else{
			if ($('.mybet').length){
				var data = []

				$('.mybet').each(function(){
					var id =  $(this).attr('name');
					var betting = $(this).val();
					data.push({ id:id, betting:betting });
				});

				var check = confirm('배팅 하시겠습니까?');
				if (check){
					$.ajax({
						url : '/user/cross/betting',
						type: 'POST',
						dataType: 'json',
						data: { 
							data: JSON.stringify(data),
							money: money_bet,
							rate: rate
						},
						success : function(resp){
							if(resp.success){
								alert('성공적으로 배팅하였습니다.');
								$('#money_crt').text(numberWithCommas(money_crt-money_bet+'원'));
							}
							else{
								alert('잘못된 접근입니다.');
							}
						},
						error : function(resp){
							console.log('server error');
						}	
					});
				}
			}
			else{
				alert('배팅한 항목이 없습니다.');
			}	
		}
	});
	//핸디캡 배팅
	$('#handicapbet_btn').click(function(){
		var money_crt = parseInt($('#money_crt').text().replace(/\,/g,''));
		var money_bet = parseInt($('#money_bet').val().replace(/\,/g,''));
		var rate = $('#rate_cml').text();
		if (money_bet > money_crt){
			alert('캐쉬가 부족합니다.');
		}
		else{
			if ($('.mybet').length){
				var data = []

				$('.mybet').each(function(){
					var id =  $(this).attr('name');
					var betting = $(this).val();
					data.push({ id:id, betting:betting });
				});

				var check = confirm('배팅 하시겠습니까?');
				if (check){
					$.ajax({
						url : '/user/handicap/betting',
						type: 'POST',
						dataType: 'json',
						data: { 
							data: JSON.stringify(data),
							money: money_bet,
							rate: rate
						},
						success : function(resp){
							if(resp.success){
								alert('성공적으로 배팅하였습니다.');
								$('#money_crt').text(numberWithCommas(money_crt-money_bet+'원'));
							}
							else{
								alert('잘못된 접근입니다.');
							}
						},
						error : function(resp){
							console.log('server error');
						}	
					});
				}
			}
			else{
				alert('배팅한 항목이 없습니다.');
			}	
		}
	});
	//스페셜 배팅
	$('#specialbet_btn').click(function(){
		var money_crt = parseInt($('#money_crt').text().replace(/\,/g,''));
		var money_bet = parseInt($('#money_bet').val().replace(/\,/g,''));
		var rate = $('#rate_cml').text();
		if (money_bet > money_crt){
			alert('캐쉬가 부족합니다.');
		}
		else{
			if ($('.mybet').length){
				var data = []

				$('.mybet').each(function(){
					var id =  $(this).attr('name');
					var betting = $(this).val();
					data.push({ id:id, betting:betting });
				});

				var check = confirm('배팅 하시겠습니까?');
				if (check){
					$.ajax({
						url : '/user/special/betting',
						type: 'POST',
						dataType: 'json',
						data: { 
							data: JSON.stringify(data),
							money: money_bet,
							rate: rate
						},
						success : function(resp){
							if(resp.success){
								alert('성공적으로 배팅하였습니다.');
								$('#money_crt').text(numberWithCommas(money_crt-money_bet+'원'));
							}
							else{
								alert('잘못된 접근입니다.');
							}
						},
						error : function(resp){
							console.log('server error');
						}	
					});
				}
			}
			else{
				alert('배팅한 항목이 없습니다.');
			}	
		}
	});
	//사다리 배팅
	$('#ladderbet_btn').click(function(){
		var money_crt = parseInt($('#money_crt').text().replace(/\,/g,''));
		var money_bet = parseInt($('#money_bet').val().replace(/\,/g,''));
		var rate = $('#rate_cml').text();
		if (money_bet > money_crt){
			alert('캐쉬가 부족합니다.');
		}
		else{
			if ($('.mybet').length == 1){
				var data = []

				var id = $('.mybet').attr('name');
				var betting = $('.mybet').val();

				var check = confirm('배팅 하시겠습니까?');
				if (check){
					$.ajax({
						url : '/user/named/ladder/betting',
						type: 'POST',
						dataType: 'json',
						data: { 
							id: id,
							betting: betting,
							money: money_bet,
							rate: rate
						},
						success : function(resp){
							if(resp.success){
								alert('성공적으로 배팅하였습니다.');
								$('#money_crt').text(numberWithCommas(money_crt-money_bet+'원'));
							}
							else{
								alert('잘못된 접근입니다.');
							}
						},
						error : function(resp){
							console.log('server error');
						}	
					});
				}
			}
			else if ($('.mybet').length > 1){
				alert('사다리는 한번에 하나의 배팅만 가능합니다.');
			}	
			else{
				alert('배팅한 항목이 없습니다.');
			}	
		}
	});

	/* 유저가 자기 정보 수정 */
	$('.mypage_modify').click(function(){
		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/user/mypage/modify',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : $('input[name="id"]').val(),
					bank : $("#bank").val(),
					bank_account : $('#bank_account').val(),
					bank_name : $("#bank_name").val()
				},
				success : function(resp){
					if(resp.success){
						alert('수정 되었습니다.');
					}
					else{
						alert('잘못된 아이디값입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	/* 유저가 쪽지 삭제 */
	$('.mypage_message_delete').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			data.push({id:tmp_id})
		});	

		var check = confirm('삭제 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/user/mypage/message/delete',
				type: 'POST',
				dataType: 'json',
				data: { 
					data: JSON.stringify(data)
				},
				success : function(resp){
					if(resp.success){
						alert('삭제 되었습니다.');
						$("input:checkbox[name=select]:checked").each(function(){
							var id = $(this).closest('tr').attr('id');
							$('#'+id).remove();
						});	
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	/* 유저 캐쉬 충전 */
	$('.charge_money').click(function(){
		var money = $('input[name="chargemoney"]').val();
		money = parseInt(money.replace(/\,/g,''));
		if (isInt(money)){
			var check = confirm('충전 요청 하시겠습니까?');
			if (check){
				$.ajax({
					url : '/user/charge',
					type: 'POST',
					dataType: 'json',
					data: { 
						chargemoney : money
					},
					success : function(resp){
						if(resp.success){
							alert('충전 요청하였습니다.');
							$('input[name="chargemoney"]').val('');
						}
						else{
							alert('잘못된 접근입니다.');
						}
					},
					error : function(resp){
						console.log('server error');
					}	
				});
			}
		}
		else{
			alert('잘못된 값입니다.');
		}
	});
	/* 유저 캐쉬 환전 */
	$('.exchange_money').click(function(){
		var money = $('input[name="exchangemoney"]').val();
		var money_crt = parseInt($('#money_crt').text().replace(/\,/g,''));
		money = parseInt(money.replace(/\,/g,''));
		if (isInt(money)){
			if (money > money_crt){ 
				alert('보유한 캐쉬보다 많은 양입니다.');
				return false;
			}
			var check = confirm('환전 요청 하시겠습니까?');
			if (check){
				$.ajax({
					url : '/user/exchange',
					type: 'POST',
					dataType: 'json',
					data: { 
						exchangemoney : money
					},
					success : function(resp){
						if(resp.success){
							alert('환전 요청하였습니다.');
							$('input[name="exchangemoney"]').val('');
							$('#money_crt').text(numberWithCommas(money_crt-money+' 원'));
						}
						else{
							alert('잘못된 접근입니다.');
						}
					},
					error : function(resp){
						console.log('server error');
					}	
				});
			}
		}
		else{
			alert('잘못된 값입니다.');
		}
	});
	/* 숫자 , 찍는 함수 */
	$('#charge1').click(function(){
		var money = $('#chargemoney').val()
		if (money == ''){
			$('#chargemoney').val(numberWithCommas(10000));
		}
		else{
			$('#chargemoney').val(numberWithCommas(parseInt(money.replace(/\,/g,''))+10000));
		}
	});
	$('#charge2').click(function(){
		var money = $('#chargemoney').val()
		if (money == ''){
			$('#chargemoney').val(numberWithCommas(50000));
		}
		else{
			$('#chargemoney').val(numberWithCommas(parseInt(money.replace(/\,/g,''))+50000));
		}
	});
	$('#charge3').click(function(){
		var money = $('#chargemoney').val()
		if (money == ''){
			$('#chargemoney').val(numberWithCommas(100000));
		}
		else{
			$('#chargemoney').val(numberWithCommas(parseInt(money.replace(/\,/g,''))+100000));
		}
	});
	$('#charge_init').click(function(){
		$('#chargemoney').val('');
	});
	$('#chargemoney').on('input',function(){
		$(this).val(numberWithCommas($(this).val().replace(/\,/g,'')));
	});	

	$('.toComma').each(function(){
		$(this).text(numberWithCommas($(this).text()));
	});	
	$('.toComma_input').each(function(){
		$(this).val(numberWithCommas($(this).val()));
	});	
	$('.toComma_input').on('input',function(){
		$(this).val(numberWithCommas($(this).val().replace(/\,/g,'')));
	});	

	$('#money_bet').on('input',function(){
		var rate_cml = parseFloat($('#rate_cml').text());
		var money = $(this).val();
		$(this).val(numberWithCommas(money.replace(/\,/g,'')));
		if(parseInt(money.replace(/\,/g,'')) > $('input[name="maxbet"]').val()){
			alert('배팅 최대액을 넘었습니다.');
			$(this).val(numberWithCommas($('input[name="minbet"]').val()));
			$('#money_cml').text(numberWithCommas(Math.round(rate_cml*$('input[name="minbet"]').val())));
		}
		else{
			if (rate_cml*parseInt(money.replace(/\,/g,'')) > $('input[name="maxgain"]').val()){
				alert('최대 당첨금을 넘습니다.');	
				$(this).val(numberWithCommas($('input[name="minbet"]').val()));
				$('#money_cml').text(numberWithCommas(Math.round(rate_cml*$('input[name="minbet"]').val())));
			}
			else{
				$('#money_cml').text(numberWithCommas(Math.round(rate_cml*parseInt(money.replace(/\,/g,'')))));
			}
		}
	});	

	/* 유저 배팅 내역 삭제 */
	$('.history_delete').click(function(){
		var id = $(this).closest('table').attr('id');
		var check = confirm('배팅 내역을 삭제하시겠습니까?');
		if (check){
			$.ajax({
				url : '/user/betting/history/delete',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id
				},
				success : function(resp){
					if(resp.success){
						alert('삭제하였습니다.');
						$('#'+id).remove();
					}
					else{
						alert('잘못된 접근입니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	/* 유저 배팅 취소 */
	$('.betting_cancel').click(function(){
		var id = $(this).closest('table').attr('id');
		var check = confirm('배팅을 취소하시겠습니까?');
		if (check){
			$.ajax({
				url : '/user/betting/cancel',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id
				},
				success : function(resp){
					if(resp.success){
						alert('취소되었습니다.');
						$('#'+id).remove();
					}
					else{
						alert(resp.msg);
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	});
	$('#levelsetting').submit(function(){
		$('.toComma_input').each(function(){
			$(this).val(parseInt($(this).val().replace(/\,/g,'')))
		});
	})
	$('.iframeContents').load(function(){
	})
	$('#article_delete').click(function(){
		var id = $('input[name="id"]').val();
		var check = confirm('해당 글을 삭제하시겠습니까?');
		if (check){
			$.ajax({
				url : '/article/delete',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id
				},
				success : function(resp){
					if(resp.success){
						alert('삭제하였습니다.');
						$(location).attr('href', '/article');
					}
					else{
						alert('작성자가 아닙니다.');
					}
				},
				error : function(resp){
					console.log('server error');
				}	
			});
		}
	})
	$('.forGain').on('input',function(){
		var id = $(this).closest('tr').attr('id');
		
		var home = parseFloat($('input[name="home_rate_'+id+'"]').val());
		var away = parseFloat($('input[name="away_rate_'+id+'"]').val());
		// 무승부도 배팅가능할때
		if ($('input[name="draw_rate_'+id+'"]').hasClass('forGain')){
			var draw = parseFloat($('input[name="draw_rate_'+id+'"]').val());
			$('#'+id).find('td.gain').text(Math.round((home+away+draw)/9*100)+'%');	
		}
		// 무승부는 배팅 불가능할때
		else{
			$('#'+id).find('td.gain').text(((home+away)/4)*100+'%');	
		}
	});	
	$('.select').each(function(){
		var id = $(this).closest('tr').attr('id');
		
		var home = parseFloat($('input[name="home_rate_'+id+'"]').val());
		var away = parseFloat($('input[name="away_rate_'+id+'"]').val());
		// 무승부도 배팅가능할때
		if ($('input[name="draw_rate_'+id+'"]').hasClass('forGain')){
			var draw = parseFloat($('input[name="draw_rate_'+id+'"]').val());
			$('#'+id).find('td.gain').text(Math.round((home+away+draw)/9*100)+'%');	
		}
		// 무승부는 배팅 불가능할때
		else{
			$('#'+id).find('td.gain').text(((home+away)/4)*100+'%');	
		}
	});	
});
function popupOpen(url, op){
	var popUrl = url;
	var popOption = op;
	window.open(popUrl, "", popOption);
}
function validateForm(){
	var x = document.forms["searchform"]["searchtext"].value;
	if (x == null || x == ""){
		alert("검색어를 입력하세요.");
		return false;
	}
}
function validateFormsearchLeague(){
	var x = document.forms["searchleague"]["league"].value;
	var y = document.forms["searchleague"]["sport"].value;
	var z = document.forms["searchleague"]["nation"].value;
	if (y == 0){
		alert("종목을 입력하세요.");
		return false;
	}
	if (z == 0){
		alert("국가를 입력하세요.");
		return false;
	}
}
function validateFormLeague(){
	var x = document.forms["addleague"]["league"].value;
	var y = document.forms["addleague"]["sport"].value;
	var z = document.forms["addleague"]["nation"].value;
	if (y == 0){
		alert("종목을 입력하세요.");
		return false;
	}
	if (z == 0){
		alert("국가를 입력하세요.");
		return false;
	}
	if (x == null || x == ""){
		alert("리그명을 입력하세요.");
		return false;
	}
}
function validateFormDetail(){
	var l = document.forms["adddetail"]["league"].value;
	var t = document.forms["adddetail"]["menu"].value;
	var s = document.forms["adddetail"]["game"].value;
	if (l == 0){
		alert('리그를 선택하세요');
		return false;
	}
	if (t == 0 || s==0){
		alert('메뉴와 게임종류를 선택하세요');
		return false;
	}
}
function validateDate(){
	var date = $('input[name="date"]').val();
	if (!moment(date, 'YYYY-M-D', true).isValid()){
		alert("날짜형식이 잘못되었습니다.");
		return false;
	}
}
function isInt(x){
	var y = parseInt(x, 10);
	return !isNaN(y) && x == y && x.toString() == y.toString();
}
function numberWithCommas(x) {
	return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
$('input, textarea').placeholder();
