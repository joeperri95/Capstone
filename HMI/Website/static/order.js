$(document).ready(function(){
  // $("#successAlert").hide();
  // $("#failedAlert").hide();
  document.getElementById("myBtn").addEventListener("click",function(){
    if(document.getElementById("Station").value == "Station" || document.getElementById("Drink").value == "Drink" || document.getElementById("FirstName").value.length == 0 || document.getElementById("LastName").value.length == 0){
      $("#failedAlert").fadeTo(2000, 500).slideUp(500, function(){
               $("#failedAlert").slideUp(500);
                });
    }
    else{
      newOrder = new Order(document.getElementById("FirstName").value,document.getElementById("LastName").value,document.getElementById("Drink").value,document.getElementById("Station").value);
      $("#successAlert").fadeTo(2000, 500).slideUp(500, function(){
               $("#successAlert").slideUp(500);
                });
    }
  });
});

function Order(first,last,drink,station){
  this.first = first;
  this.last = last;
  this.drink = drink;
  this.station = station;
}
