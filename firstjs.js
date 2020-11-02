//Function for checking speed
function checkSpeed(){
  //Get values from input fields
  var speed = Number(document.getElementById("theSpeed").value);
  //Actual speed limit value
  var speed_limit = Number(document.getElementById("speedlimit").value);

  console.log("Logs: " + String(speed_limit));

  //Check if speed is greater than speed_limit
  if(speed > speed_limit){
    var output = "<center><h3 style ='color:red'>Slow down! You're speeding.</h3></center>";
    document.getElementById("output").innerHTML = output;
  }

  //If they aren't speeding
  if(speed < speed_limit){
    var output = "<center><h3 style ='color:green'>Good job! You are not speeding.</h3></center>";
    document.getElementById("output").innerHTML = output;
  }

  //Prepare data for sending
  var data = "speed=" + encodeURIComponent(speed);
  //SECOND value
  data += "&limit=" + encodeURIComponent(speed_limit);
  // POST data to Python server
  fetch("http://localhost:8080/speed", {
    method: "POST",
    body: data,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
  //Once the response is obtained
  }).then(function (response) {
    console.log("Done!");
    console.log(response);
  });
}

function view_prev(){
  fetch("http://localhost:8080/previous", {
    method: "GET",
    mode: 'cors'
  //Once the response is obtained
  }).then(function (response) {
    console.log("Done!");
    console.log(response.statusText);
    document.getElementById('output1').innerHTML = response.statusText;
  });
}
