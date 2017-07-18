$(document).ready(function(){
    $('#foo').multiDatesPicker();
    $('#send').bind('click', function() {
    	var dates = document.getElementById('foo').value.split(',');
    	for (date of dates.entries()) {
    		alert('date#' + date[0] + ': ' + date[1])
    	}
    });
});

