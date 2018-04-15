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
    // console.log("hover");
    $(this).css("color", "rgb(80, 204, 127)");
  }, function(){
    $(this).css("color", "black");
  });

  $(document).on("click", ".comment_text, .expand_wrap", function(){
    // console.log("toggle")
    var id = $(this).attr("pkid");
    comToggle(id);
  });

  $(document).on("click", ".comment_up", function(){
    var com_id = $(this).attr("pkid");
    handlersOff();
    // console.log("up");
    comvote(com_id, 1);
  });

  $(document).on("click", ".comment_down", function(){
    var com_id = $(this).attr("pkid");
    handlersOff();
    // console.log("down");
    comvote(com_id, -1);
  });

  $(document).on("submit", "#comment_form", function(event){
    event.preventDefault();
    handlersOff();
    // console.log("new com");
    create_comment();
  });

});

$(document).ajaxStop(function() {

    $(".comment_up, .comment_down").hover(function(){
      // console.log("hover");
      $(this).css("color", "rgb(80, 204, 127)");
    }, function(){
      $(this).css("color", "black");
    });
  });


  function comToggle(parid) {
    // console.log("toggling")
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
        // console.log(data["points"])
        $("#compoints_"+com_id).text(data["points"]);
      }
    });
  }

  function create_comment(){
    $.ajax({
      type: "POST",
      url: "/create_comment/",
      data: {
        'text': $("#comment_area").val(),
        'parent_mod': $("#comment_form").attr("module"),
      },
      success: function(){
        $("#com_load").load("/solution/ .comments");
      }
    });
  }

  function handlersOff(){
    $(".comment_down, .comment_up").off("click")
    $(".comment_text, .expand_wrap").off("click");
    $("#comment_form").off("submit");
    $(".comment_up, .comment_down").off("mouseenter mouseleave");
  }
