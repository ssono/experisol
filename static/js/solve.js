$(document).ready(function(){
  $(".post_up, .post_down, .post_fav").hover(function(){
    $(this).css("color", "rgb(80, 100, 220)");
  }, function(){
    $(this).css("color", "rgb(80, 204, 127)");
  });

  $(".comment_up, .comment_down").hover(function(){
    $(this).css("color", "rgb(80, 204, 127)");
  }, function(){
    $(this).css("color", "black");
  });
});
