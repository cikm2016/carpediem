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
						$('#'+id).empty();	
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
						$('#'+id).empty();	
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
	$('.chk_login').click(function(){
		var id = $(this).closest('tr').attr('id');
		popupOpen('/admin/user/loginlog/'+id, 'width=800, height=800, resizable=yes,scrollbars=yes;');
	});
	$('.detail').click(function(){
		var id = $(this).closest('tr').attr('id');
		popupOpen('/admin/user/detail/'+id, 'width=800, height=800, resizable=yes,scrollbars=yes;');
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
					level : $("#level").val(),
					state : $('#state').val(),
					danger : $("#danger").val()
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
		var name = $('input[name="'+id+'"]').val();
		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/sport/modify',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					name : name 
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
						$('#'+id).empty();
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
		var name = $('input[name="'+id+'"]').val();
		var check = confirm('수정 하시겠습니까?');
		if (check){
			$.ajax({
				url : '/admin/league/nation/modify',
				type: 'POST',
				dataType: 'json',
				data: { 
					id : id,
					name : name 
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
						$('#'+id).empty();
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
		var name = $('input[name="'+id+'"]').val();
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
						$('#'+id).empty();
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
	$('.detail_modify').click(function(){
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
					away : $('input[name="away_'+id+'"]').val()
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
	$('.detail_delete').click(function(){
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
						$('#'+id).empty();
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
	$('select[name="game"]').change(function(){
		var game = $('select[name="game"]').val();
		var i;
		var date_first = $('input[name="date_first"]').val();
		var date_second = $('input[name="date_second"]').val();
		var league_name = $('select[name="league"] option:selected').text();
		if (date_first == "" || date_second == ""){
			alert('경기날짜와 시간을 입력하세요.');
			return false;
		}	
		else{
			$('.addlist').empty();
			for (i=0;i<game;i++){
				var str = '<tr> <td><input type="text" class="form-control" name="date_first_'+i+'" value="'+date_first+'"></td> <td><input type="text" class="form-control" name="date_second_'+i+'" value="'+date_second+'"></td> <td><input type="text" class="form-control" name="league_'+i+'" value="'+league_name+'" disabled></td> <td><input type="text" class="form-control home" name="home_'+i+'"></td> <td><input type="text" class="form-control away" name="away_'+i+'"></td> </tr>'
				$('.addlist').append(str);	
			}		
			if (game == 0){
				$('#addgamebtn').hide();
			}
			else{
				$('#addgamebtn').show();
			}
		}
		
	});
	// 등록 경기 수정
	$('.game_modify').click(function(){
		var id = $(this).closest('tr').attr('id');

		var check = confirm('수정 하시겠습니까?');
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
						$('#'+id).empty();
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
	$('.game_all_apply').click(function(){
		var data = []
		$("input:checkbox[name=select]:checked").each(function(){
			var tmp_id = $(this).closest('tr').attr('id');
			var tmp_home = $('#'+tmp_id).find('input[name="home_rate_'+tmp_id+'"]').val();
			var tmp_draw = $('#'+tmp_id).find('input[name="draw_rate_'+tmp_id+'"]').val();
			var tmp_away = $('#'+tmp_id).find('input[name="away_rate_'+tmp_id+'"]').val();
			data.push({id:tmp_id, home:tmp_home, draw:tmp_draw, away:tmp_away})
		});	
		var check = confirm('수정 하시겠습니까?');
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
							$('#'+id).empty();
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
			data.push({id:tmp_id, state:tmp_state})
		});	

		var check = confirm('수정 하시겠습니까?');
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
						$('#'+id).empty();
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
							$('#'+tmp_id).empty();
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
	$('.select').click(function(){
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
						$('#'+id).empty();
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
						$('#'+id).empty();
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
	$(".clickbox").hover(
		function(){
			$(this).css("border-color","red");
			$(this).css("cursor","pointer");
		},
		function(){ 
			$(this).css("border-color","black");
		}
	);
	$(".clickbox").click(function(){
		var id = $(this).closest('tr').attr('id');

		var money_cml = $('#money_cml').val();
		var rate_cml = $('#rate_cml').val();
		var money_bet = $('#money_bet').val();

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
			$(this).removeClass('clicked');
		}
		/* 새로운팀 클릭 */
		else{
			var clicked = $('#'+id).find('td.clicked')
			/* 클릭된 팀이 없을때 */
			if (clicked.text() == ""){
				if (rate_cml == 0){
					ret_rate = rate;
				}
				else{
					ret_rate = rate_cml*rate;
				}
				$(this).addClass('clicked');
				var betteam = '<tr id="bet_'+id+'"><td>'+rate+'</td><td>'+team+'</td></tr>';
				$('.bet_table').append(betteam);
				
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
				clicked.removeClass('clicked');
				$(this).addClass('clicked');
				$('#bet_'+id).remove();
				var betteam = '<tr id="bet_'+id+'"><td>'+rate+'</td><td>'+team+'</td></tr>';
				$('.bet_table').append(betteam);
			}
		}
		$('#rate_cml').val(ret_rate.toFixed(2));
		$('#money_cml').val(Math.round(ret_rate*money_bet));
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
							$('#'+id).empty();
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
function validateFormIp(){
	var x = document.forms["ipform"]["ip2"].value;
	if (x == null || x == ""){
		alert("아이피를 입력하세요.");
		return false;
	}
}
function validateFormLeague(){
	var x = document.forms["addleague"]["league"].value;
	if (x == null || x == ""){
		alert("리그명을 입력하세요.");
		return false;
	}
}
function validateFormDetail(){
	var x = document.forms["adddetail"]["name"].value;
	var y = document.forms["adddetail"]["home"].value;
	var z = document.forms["adddetail"]["away"].value;
	if (x == "" ||y == "" ||z == "" ){
		alert("값을 입력하세요.");
		return false;
	}
}
function isInt(x){
	var y = parseInt(x, 10);
	return !isNaN(y) && x == y && x.toString() == y.toString();
}