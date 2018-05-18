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
    $(this).css("color", "rgb(210, 230, 230)");
    }, function(){
    $(this).css("color", "rgb(80, 204, 127)");
  });

  $(".glyphicon-menu-right, .glyphicon-menu-left").hover(function(){
    console.log("scroll")
    $(this).css("color", "rgb(210, 230, 230)");
    }, function(){
    $(this).css("color", "rgb(80, 204, 127)");
  });

  $("#mod_bar_wrap").on("click", ".glyphicon-menu-right", function(){
    console.log("next_post");
    var id = $(this).attr("pkid");
    get_next_mod(id);
  });

  $(".comment_up, .comment_down").hover(function(){
    console.log("hover");
    $(this).css("color", "rgb(80, 204, 127)");
  }, function(){
    $(this).css("color", "black");
  });

  $("#com_wrap").on("click", ".comment_text, .expand_wrap", function(){
    console.log("toggle")
    var id = $(this).attr("pkid");
    comToggle(id);
  });

  $("#com_wrap").on("click", ".reply_wrap", function(){
    var id = $(this).attr("pkid");
    replyToggle(id);
  });

  $("#com_wrap").on("click", ".comment_up", function(){
    var com_id = $(this).attr("pkid");
    handlersOff();
    console.log("up");
    comvote(com_id, 1);
  });

  $("#com_wrap").on("click", ".comment_down", function(){
    var com_id = $(this).attr("pkid");
    handlersOff();
    console.log("down");
    comvote(com_id, -1);
  });

  $("#com_wrap").on("submit", "#comment_form", function(event){
    event.preventDefault();
    handlersOff();
    console.log("new com");
    create_comment();
  });

  $("#com_wrap").on("submit", ".reply_form", function(event){
    event.preventDefault();
    var id = $(this).attr("com_par");
    handlersOff();
    console.log("new rep");
    create_reply(id);
  });

});

$(document).ajaxStop(function() {

    $(".comment_up, .comment_down").hover(function(){
      console.log("hover");
      $(this).css("color", "rgb(80, 204, 127)");
    }, function(){
      $(this).css("color", "black");
    });

    $(".glyphicon-menu-right, .glyphicon-menu-left").hover(function(){
      console.log("scroll")
      $(this).css("color", "rgb(210, 230, 230)");
    }, function(){
      $(this).css("color", "rgb(80, 204, 127)");
    });

  });


  function comToggle(parid) {
    console.log("comtog");
    $(".par"+parid).toggle();
  }

  function replyToggle(comid) {
    console.log("reptog");
    $("#reply_"+comid).toggle();
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
        console.log(data["points"])
        $("#compoints_"+com_id).text(data["points"]);
      }
    });
  }

function create_comment(){
  var id = $("#current_module").attr("pkid");
  var current_url = "/solution/"+id+"/";
  $.ajax({
    type: "POST",
    url: "/create_comment/",
    data: {
      'text': $("#comment_area").val(),
      'parent_mod': $("#comment_form").attr("module"),
    },
    success: function(){
      $("#com_wrap").load(current_url + " .comments");
    }
  });
}

function create_reply(com_id){
  var mod_id = $("#current_module").attr("pkid");
  var current_url = "/solution/"+mod_id+"/";
  $.ajax({
    type: "POST",
    url: "/create_reply/",
    data: {
      'text': $("#reply_area" + com_id).val(),
      'parent_com': com_id,
    },
    success: function(){
      $("#com_wrap").load(current_url + " .comments");
    }
  });
}

function get_next_mod(id){
  var get_next = "/solution/next/" + id + "/"
  $.ajax({
    type: "GET",
    url: get_next,
    success: function(data){
      var mod_url = "/solution/"+data['new_pk'] + "/";
      $("#mod_bar_wrap").load(mod_url+ " .module_bar");
      $("#com_wrap").load(mod_url + " .comments");
      $("#section_wrap").load(mod_url + " .sections");
      history.pushState(null,null, mod_url);
    }
  });
}


function handlersOff(){
  $(".comment_down, .comment_up").off("click");
  $(".comment_text, .expand_wrap").off("click");
  $(".reply_wrap").off("click");
  $("#comment_form").off("submit");
  $(".comment_up, .comment_down, .glyphicon-menu-right, .glyphicon-menu-left").off("mouseenter mouseleave");
}

//go left, comments
