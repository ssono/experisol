$(document).ready(function(){
  $("#enter").hover(function(){
    $(this).css("background-color", "rgb(80, 204, 127)");
    $(this).css("color", "black");
  }, function(){
    $(this).css("background-color", "rgb(5,55,75)");
    $(this).css("color", "rgb(80, 204, 127)");
  });
});
