function showImage(name, txt){
	var img = document.getElementById("imageBelow");
	img.src = name;
	img.alt = txt;
}

function showThumbnail(name, txt, id){
	var img = document.getElementById(id);
	img.src = name;
	img.alt = txt;
}