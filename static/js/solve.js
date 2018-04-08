$(document).ready(function(){
  $(".post-up, .post-down, .post-fav").hover(function(){
    $(this).css("color", "rgb(80, 204, 127)");
  }, function(){
    $(this).css("color", "rgb(140, 170, 180)");
  });

  $(".comment-up, .comment-down").hover(function(){
    $(this).css("color", "rgb(80, 204, 127)");
  }, function(){
    $(this).css("color", "black");
  });
});
