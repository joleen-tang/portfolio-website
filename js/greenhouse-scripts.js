var buyable = ['Mixed Herb Seeds', 'Western Fodlan Seeds', 'Root Vegetable Seeds', 'Vegetable Seeds', 
	'Northern Fodlan Seeds', 'Southern Fodlan Seeds', 'Eastern Fodlan Seeds', 'Red Flower Seeds', 'White Flower Seeds',
	'Blue Flower Seeds', 'Purple Flower Seeds', 'Yellow Flower Seeds', 'Green Flower Seeds', 'Pale-Blue Flower Seeds'];

function selectBuyable(){
	for (seed in buyable){
		var node = $("input[value='"+buyable[seed]+"']");
		if (node.length){
			node.prop("checked", true);
		}
	}
}
