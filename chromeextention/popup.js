document.addEventListener( 'DOMContentLoaded', function(){
	chrome.tabs.getSelected( null, function(tab){
		var xhr = new XMLHttpRequest(), c, d;
		xhr.open("GET", 'http://api.ligo.kr/?url=' + encodeURIComponent(tab.url), false), xhr.send(),
		d = xhr.responseText,
		document.getElementById('url').value = d,
		( c = document.getElementById('copy') ).innerHTML = 'Copy',
		c.addEventListener( 'click', function(){
			document.getElementById('url').select(),
			document.execCommand( 'copy', false, null ),
			window.close();
		} );
	} );
});