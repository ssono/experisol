$(document).ready(function(){
  $(".tryit").hover(function(){
    $(this).css("background-color", "rgb(0,242,143)");
    $(this).css("color", "black");
    $(this).css("border-color", "black");
  }, function(){
    $(this).css("background-color", "rgb(0,220,130)");
    $(this).css("color", "rgb(0,50,80)");
    $(this).css("border-color", "rgb(0,50,80)");

  });

  $(".email_but").hover(function(){
      $(this).css("background-color", "rgb(0,40,64)");
      $(this).css("color", "rgb(0,242,143)");
      $(this).css("border-color", "rgb(0,242,143)");
    }, function(){
      $(this).css("background-color", "rgb(0,50,80)");
      $(this).css("color", "rgb(0,220,130)");
      $(this).css("border-color", "rgb(0,220,130)");
    });
});
