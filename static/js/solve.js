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

  $(".comment_text").click(function(){
    var id = $(this).attr("pkid");
    comToggle(id);
  });

  $(".comment_up").click(function(){
    var com_id = $(this).attr("pkid");
    $.ajax({
      type: "POST",
      url: "/com_up/",
      data: {
          'com_id': com_id
      },
      success: function(){
        $(".com_"+String(com_id)).load('/solution/');
      }
    });
  });
});

function comToggle(parid) {
  $(".par"+parid).toggle();
}
