function addEventListeners(){
}

function toggleNavDisplay(elementId){
	var element=document.getElementById(elementId);
	if (element.style.display=="none"){
		element.style.width="15%";
		element.nextElementSibling.style.width="85%";
		element.style.display="inline-block";
		return;
	} else{
	element.style.width="0%";
	element.nextElementSibling.style.width="100%";
	element.style.display="none";
	}
}
