console.clear();
var mymap = L.map('mapid').setView([55.7344, 37.598], 15);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(mymap);
var crd;
var coordsJSON;
var json;

var originArr = [];
var originArr2 = [];

//building raw route
function createRoute(){
    var polyline = L.polyline(originArr, {color: '#e53935', dashArray: '6'}).addTo(mymap);
    var circle = L.circle(originArr[originArr.length-1], {color: '#e53935', fillColor: '#e53935', fillOpacity: 0.2, radius: 200}).addTo(mymap);
    var circle = L.circle(originArr[originArr.length-2], {color: '#e53935', fillColor: '#e53935', fillOpacity: 0.2, radius: 200}).addTo(mymap);
    var circle = L.circle(originArr[originArr.length-1], {color: '#e53935', fillColor: '#e53935', fillOpacity: 1, radius: 2}).addTo(mymap);
    var circle = L.circle(originArr[originArr.length-2], {color: '#e53935', fillColor: '#e53935', fillOpacity: 1, radius: 2}).addTo(mymap);
    document.getElementById( "improve" ).setAttribute( "onClick", "javascript: createRoute_2();" );
}

function change()
{
   document.getElementById("improve").textContent="Improve";
}
//building corrected route
var createRoute_2 = function(){
        document.getElementById( "improve" ).setAttribute( "onClick", "javascript: done();" );
    var polyline = L.polyline(originArr2, {color: '#1976d2', dashArray: '10'}).addTo(mymap);
    var circle = L.circle(originArr[originArr2.length-1], {color: '#1976d2', fillColor: '#1976d2', fillOpacity: 0.2, radius: 40}).addTo(mymap);
    var circle = L.circle(originArr[originArr2.length-2], {color: '#1976d2', fillColor: '#1976d2', fillOpacity: 0.2, radius: 40}).addTo(mymap);
    var circle = L.circle(originArr[originArr2.length-1], {color: '#1976d2', fillColor: '#1976d2', fillOpacity: 1, radius: 2}).addTo(mymap);
    var circle = L.circle(originArr[originArr2.length-2], {color: '#1976d2', fillColor: '#1976d2', fillOpacity: 1, radius: 2}).addTo(mymap);
    document.getElementById("improve").textContent="Done!";
}

  

//parsing raw dots coords
  fetch( 'http://www.json-generator.com/api/json/get/bVzuQPiYya?indent=2' ).then( function (response) {
	return response.json();
}) .then(function (obj) {
    for (var i = 0; i<obj.length; i++){
    var iO = [obj[i].latitude, obj[i].longitude];
    originArr.push(iO);
}




}) .catch( function (error) {
	console.error( 'Что-то пошло не так. Ошибка.');
	console.error(error);
});

//parsing corrected by ML dots coords
fetch( 'http://www.json-generator.com/api/json/get/bVzuQPiYya?indent=2' ).then( function (response) {
	return response.json();
}) .then(function (obj) {
    for (var i = 0; i<obj.length; i++){
    var iO = [obj[i].latitude, obj[i].longitude];
    originArr2.push(iO);
}




}) .catch( function (error) {
	console.error( 'Что-то пошло не так. Ошибка.');
	console.error(error);
});