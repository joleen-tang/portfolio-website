const BUYABLE = ['1', '2', '3', '4', '5', '7', '12', '15', '16', '17', '18', '19', '20', '21'];

const TABLE_HEADER = "<tr><th>Score</th><th>Cultivation Level</th>"+
	'<th class="seed-col">Seed 1</th><th class="qty-col">Qty</th>'+
	'<th class="seed-col">Seed 2</th><th class="qty-col">Qty</th>'+
	'<th class="seed-col">Seed 3</th><th class="qty-col">Qty</th>'+
	'<th class="seed-col">Seed 4</th><th class="qty-col">Qty</th>'+
	'<th class="seed-col">Seed 5</th><th class="qty-col">Qty</th></tr>';


// Functionality for 'Select All Buyable Seeds' button
function selectBuyable(){
	for (seed in BUYABLE){
		let node = $("input[value='"+BUYABLE[seed]+"'][name='usable']");
		if (node.length){
			node.prop("checked", true);
		}
	}
}


// Functionality for 'Deselect All' seeds button
function deselectAll(){
	let seeds = $("input[name='usable']")
	for (seed in seeds){
		seeds[seed].checked=false;
	}
}


// Checking that there are seeds available to build a combo from
function validateSeeds(){
	let seeds = $("input[name='usable']")
	for (seed in seeds){
		if (seeds[seed].checked){
			hideError('seed-error');
			return true;
		}
	}
	showError('seed-error');
	event.preventDefault();
	return false;
}


function showError(errorName){
	let error = $("."+errorName);
	error[0].style.display="inline-block";
}


function hideError(errorName){
	let error = $("."+errorName);
	error[0].style.display="none";
}


function validateUnwanted(){
	let unwanted = $("input[name='unwanted']");
	for (i in unwanted){
		if (unwanted[i].checked){
			let checkPriority = $("#"+unwanted[i].value);
			let checkPriority2 = $("#"+unwanted[i].value+"2");
			if (checkPriority[0].checked || checkPriority2[0].checked){
				showError('unwanted-error');
				event.preventDefault();
				return false;
			}
		}
	}
	hideError('unwanted-error');
	return true;
}


$(document).ready(function(){$("#greenhouse-form-button").click(function(event){
		var form = $("#greenhouse-form");
		var formID = "greenhouse-form";
		var url = form.prop('action');
		var type = form.prop('method');
		var formData = getFormData(formID);

		sendForm(form, url, type, formData);
	})
})


function getFormData(formID){
	return new FormData(document.getElementById(formID))
}


function sendForm(form, url, type, formData){
	let seedVal = validateSeeds();
	let unwantedVal = validateUnwanted();
	if (form[0].checkValidity() && seedVal && unwantedVal){
		event.preventDefault();
		$("#results table tbody")[0].style.display="none";
		$("#results table tbody")[0].innerHTML=TABLE_HEADER;
		$("#results p")[0].innerHTML="Please wait a moment...";
		$("#results p")[0].style.display="block";
		$("#results")[0].style.display="block";

		modularAjax(url, type, formData);
	}
}


function modularAjax(url, type, formData){
	$.ajax({
		url: url,
		type: type,
		data: formData,
		processData: false,
		contentType: false,
		dataType: "text",
		success: function(data){
			var results = $("#results table")[0];
			if (data.length == 0){
				$("#results p")[0].innerHTML="No combinations were found; try a different set of filters";
			}
			else{
				$("#results table tbody")[0].innerHTML += data;
				$("#results p")[0].style.display="none";
				$("#results")[0].style.display = "block";
				$("#results table")[0].style.display = "table";
				$("#results table tbody")[0].style.display="table-row-group";
			}
		}
	})
}

