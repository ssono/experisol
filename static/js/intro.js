$(document).ready(function(){
  $("#enter").hover(function(){
    $(this).css("background-color", "rgb(80, 204, 127)");
    $(this).css("color", "black");
  }, function(){
    $(this).css("background-color", "rgb(0,220,130)");
    $(this).css("color", "rgb(0,50,80)");
  });
});
