const buyable = ['Mixed Herb Seeds', 'Western Fodlan Seeds', 'Root Vegetable Seeds', 'Vegetable Seeds', 
	'Northern Fodlan Seeds', 'Southern Fodlan Seeds', 'Eastern Fodlan Seeds', 'Red Flower Seeds', 'White Flower Seeds',
	'Blue Flower Seeds', 'Purple Flower Seeds', 'Yellow Flower Seeds', 'Green Flower Seeds', 'Pale-Blue Flower Seeds'];


// Functionality for 'Select All Buyable Seeds' button
function selectBuyable(){
	for (seed in buyable){
		let node = $("input[value='"+buyable[seed]+"']");
		if (node.length){
			node.prop("checked", true);
		}
	}
}


// Checking that there are seeds available to build a combo from
function validateSeeds(){
	let seeds = $("input[name='usable']")
	for (seed in seeds){
		if (seeds[seed].checked){
			hideError('seed-error');
			return;
		}
	}
	showError('seed-error');
	event.preventDefault();
}


function showError(error_name){
	let error = $("."+error_name);
	error[0].style.display="inline-block";
}


function hideError(error_name){
	let error = $("."+error_name);
	error[0].style.display="none";
}


function validateUnwanted(){
	let unwanted = $("input[name='unwanted']");
	for (i in unwanted){
		if (unwanted[i].checked){
			console.log(unwanted[i].value);
			let check_priority = $("#"+unwanted[i].value);
			let check_priority2 = $("#"+unwanted[i].value+"2");
			if (check_priority[0].checked || check_priority2[0].checked){
				showError('unwanted-error');
				event.preventDefault();
				return;
			}
		}
	}
	hideError('unwanted-error');
}


// Adding event listeners to form
$(document).ready(function(){
	let forms = $("form")
	for (i = 0; i < forms.length; i++){
		forms[i].addEventListener("submit", validateSeeds)
		forms[i].addEventListener("submit", validateUnwanted)
	}
})
