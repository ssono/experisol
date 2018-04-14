function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

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

  $(".comment_text, .expand_wrap").click(function(){
    var id = $(this).attr("pkid");
    comToggle(id);
  });

  $(".comment_up").click(function(){
    var com_id = $(this).attr("pkid");
    var weight = 1;
    comvote(com_id, weight);
  });

  $(".comment_down").click(function(){
    var com_id = $(this).attr("pkid");
    var weight = -1;
    comvote(com_id, weight);
  });
});

function comToggle(parid) {
  $(".par"+parid).toggle();
}

//vote weight determines up/down and by how much
function comvote(com_id, weight){
  $.ajax({
    type: "POST",
    url: "/com_vote/",
    data: {
        'com_id': com_id,
        'weight': weight,
    }, dataType: "json",
    success: function(data){
      $("#compoints_"+com_id).text(data["points"]);
    }
  });
}
