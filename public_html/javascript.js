var data;
var size;
var json;
var index;
function fun()
{
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "http://ec2-18-221-131-219.us-east-2.compute.amazonaws.com:5000/search", true);
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        index=0;
        json = JSON.parse(xhr.responseText);
        console.log(json.previous_occurence + ", " + json.best_guess);
		document.getElementById('previous_occurence').innerHTML = "Previously Appeared: "+json.previous_occurence;
		document.getElementById('best_guess').innerHTML = "Best Guess: "+json.best_guess;
		document.getElementById('links').innerHTML = "Links: "+json.links[index];
		document.getElementById('descriptions').innerHTML = "Descriptions: "+json.descriptions[index];
    }
	};
	data = JSON.stringify({"image_url": document.getElementById("image_url").value});
    console.log(document.getElementById("image_url").value);
	xhr.send(data);
}
function next()
{
	index=index+1;
	document.getElementById('links').innerHTML = "Links: "+json.links[index];
	document.getElementById('descriptions').innerHTML = "Descriptions: "+json.descriptions[index];	
}
