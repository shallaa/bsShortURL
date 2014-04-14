document.addEventListener( 'DOMContentLoaded', function(){
	chrome.tabs.getSelected( null, function(tab){
		var xhr = new XMLHttpRequest(), c, d;
		xhr.open("GET", 'http://jsonp.ligo.kr/?callback=callback&url=' + encodeURIComponent(tab.url), false), xhr.send(),
		d = JSON.parse( xhr.responseText.substring('callback('.length, xhr.responseText.length - 1 ) ).data,
		document.getElementById('url').value = d, 
		( c = document.getElementById('copy') ).innerHTML = 'Copy',
		c.addEventListener( 'click', function(){
			document.getElementById('url').select(),
			document.execCommand( 'copy', false, null ),
			window.close();
		} );
	} );
});