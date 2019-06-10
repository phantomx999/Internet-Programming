function checkInput() {
	var eve = document.getElementById("eventID").value;
	var loc = document.getElementById("locationID").value;
	
	if( (eve.match(/^[A-Za-z_0-9]+$/)) && (loc.match(/^[A-Za-z_0-9]+$/)) ){
		return true;
	}
	else{
		alert("Event name and Location name must be alphanumeric")
		return false;
	}
}
