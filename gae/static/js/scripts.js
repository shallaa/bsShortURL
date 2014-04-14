bs( function() {
	var tLink = '';
	
	function submitShor(){
		bs.Dom('#loading').S('display', 'block');
		
		bs.post(function(data, err) {
			var str = '';
		
			if (data.indexOf('ligo.kr') != -1){
				tLink = data;
				str = '<a href="' + data + '" target="_blank"><strong>' + data + '</strong></a>';
				bs.Dom('#socialBtns').S('display', 'block');
			} else {
				tLink = '';
				str = '<strong>' + data + '</strong>';
				bs.Dom('#socialBtns').S('display', 'none');
			}
			
			bs.Dom('#pres').S('html', str);
			bs.Dom('#loading').S('display', 'none');
		}, '/', 'url', bs.Dom('#url').S('@value'));
	}
	
	bs.Dom('#btnShort').S('click', function() {
		submitShor();
	});
	
	bs.Dom('#btnFb').S('click', function() {
		if (tLink != '') {
			bs.open("https://www.facebook.com/sharer/sharer.php?u=" + tLink);
		}
	});
	
	bs.Dom('#btnTw').S('click', function() {
		if (tLink != '') {
			bs.open("https://twitter.com/intent/tweet?text=" + tLink);
		}
	});
	
	bs.Dom('#btnGp').S('click', function() {
		if (tLink != '') {
			bs.open("https://plus.google.com/share?url=" + tLink);
		}
	});
} );