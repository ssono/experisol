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
    turnshitoff();
    console.log("vote n");
    comvote(com_id, 1);
  });

  $(".comment_down").click(function(){
    var com_id = $(this).attr("pkid");
    console.log("vote n");
    turnshitoff();
    comvote(com_id, -1);
  });

  $("#comment_form").submit(function(event){
    event.preventDefault();
    console.log("click successful n");
    turnshitoff();
    create_comment()
    //$.getScript("/static/js/solve.js");
  });

});

function comToggle(parid) {
  console.log("toggling")
  $(".par"+parid).toggle();
}

//vote weight determines up/down and by how much
function comvote(com_id, weight){
  turnshitoff();
  $.ajax({
    type: "POST",
    url: "/com_vote/",
    data: {
        'com_id': com_id,
        'weight': weight,
    }, dataType: "json",
    success: function(data){
      console.log(data["points"])
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

function turnshitoff(){
  $(".comment_down, .comment_up").off("click")
  $(".comment_text, .expand_wrap").off("click");
  $("#comment_form").off("submit");
}

$(document).ajaxStop(function() {

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
      turnshitoff();
      console.log("vote a")
      comvote(com_id, 1);
    });

    $(".comment_down").click(function(){
      var com_id = $(this).attr("pkid");
      turnshitoff();
      console.log("vote a")
      comvote(com_id, -1);
    });

    $("#comment_form").submit( function(event){
      turnshitoff();
      event.preventDefault();
      console.log("click successful a");
      create_comment()
      turnshitoff();
      $.getScript("/static/js/solve.js");
      turnshitoff();
    });

});
