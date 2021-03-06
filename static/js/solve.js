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

var active_reply = 0;

$(document).ready(function(){
  // console.log(active_reply);

  $(window).on("popstate", function(){
    // console.log("pop");
    location.reload();
  });


  $(".post_up, .post_fav").hover(function(){
    $(this).css("color", "rgb(210, 230, 230)");
    }, function(){
    $(this).css("color", "rgb(80, 204, 127)");
  });

  $(".glyphicon-menu-right, .glyphicon-menu-left").hover(function(){
    // console.log("scroll")
    $(this).css("color", "rgb(210, 230, 230)");
    }, function(){
    $(this).css("color", "rgb(80, 204, 127)");
  });

  $("#mod_bar_wrap").on("click", ".glyphicon-menu-right", function(){
    // console.log("next_post");
    var id = $(this).attr("pkid");
    get_next_mod(id);
  });

  $("#mod_bar_wrap").on("click", ".glyphicon-menu-left", function(){
    // console.log("prev_post");
    var id = $(this).attr("pkid");
    get_prev_mod(id);
  });

  $(document).keydown(function(e){
    if(active_reply != 0){
      reply = "reply_area" + active_reply;
    }
    if(document.getElementById("comment_area").value == '' && active_reply == 0){
      var id = $("#current_module").attr("pkid");
      if(document.getElementById("comment_area").value == ''){
        reply = "reply_area" + active_reply;

        if (e.keyCode == 39){
          get_next_mod(id);
        } if (e.keyCode == 37){
          get_prev_mod(id);
        }
      }
    }
  });

  $(".comment_up, .comment_down").hover(function(){
    // console.log("hover");
    $(this).css("color", "rgb(80, 204, 127)");
  }, function(){
    $(this).css("color", "black");
  });

  $("#post_vote").on("click", ".post_up", function(){
    var proj_id = $("#page_info").attr("proj_pk");
    handlersOff();
    projvote(proj_id);
    // console.log(document.getElementById("prupvote").classList);
    document.getElementById("prupvote").classList.remove("post_up");
    // console.log(document.getElementById("prupvote").classList);
    $(this).css("color", "rgb(210, 230, 230)");
  });

  $("#com_wrap").on("click", ".comment_text, .expand_wrap", function(){
    // console.log("toggle")
    var id = $(this).attr("pkid");
    comToggle(id);
  });

  $("#com_wrap").on("click", ".reply_wrap", function(){
    var id = $(this).attr("pkid");
    // console.log(id);
    active_reply = id;
    // console.log(active_reply)
    replyToggle(id);
  });

  $("#com_wrap").on("click", ".comment_up", function(){
    var com_id = $(this).attr("pkid");
    handlersOff();
    // console.log("up");
    comvote(com_id, 1);
    document.getElementById("up"+com_id).classList.remove("comment_up");
    $(this).css("color", "rgb(80,204,127)");
  });

  // $("#com_wrap").on("click", ".comment_down", function(){
  //   var com_id = $(this).attr("pkid");
  //   handlersOff();
  //   // console.log("down");
  //   comvote(com_id, -1);
  // });

  $("#com_wrap").on("submit", "#comment_form", function(event){
    event.preventDefault();
    handlersOff();
    // console.log("new com");
    create_comment();
  });

  $("#com_wrap").on("submit", ".reply_form", function(event){
    event.preventDefault();
    active_reply = 0;
    var id = $(this).attr("com_par");
    handlersOff();
    // console.log("new rep");
    create_reply(id);
  });

});

$(document).ajaxStop(function() {

  $(".comment_up, .comment_down").hover(function(){
      // console.log("hover");
      $(this).css("color", "rgb(80, 204, 127)");
    }, function(){
      $(this).css("color", "black");
  });

  $(".glyphicon-menu-right, .glyphicon-menu-left").hover(function(){
      // console.log("scroll")
      $(this).css("color", "rgb(210, 230, 230)");
    }, function(){
      $(this).css("color", "rgb(80, 204, 127)");
    });

    $(".post_up, .post_fav").hover(function(){
        $(this).css("color", "rgb(210, 230, 230)");
      }, function(){
        $(this).css("color", "rgb(80, 204, 127)");
    });

  });

  $(".post_up, .post_fav").hover(function(){
      $(this).css("color", "rgb(210, 230, 230)");
    }, function(){
      $(this).css("color", "rgb(80, 204, 127)");
  });

  function comToggle(parid) {
    // console.log("comtog");
    $(".par"+parid).toggle();
  }

  function replyToggle(comid) {
    // console.log("reptog");
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
        // console.log(data["points"])
        $("#compoints_"+com_id).text(data["points"]);
      }
    });
  }

  function projvote(proj_id){
    $.ajax({
      type: "POST",
      url: "/proj_vote/",
      data: {
          'proj_id': proj_id,
      }, dataType: "json",
      success: function(data){
        // console.log(data["points"])
        $("#ppoints").text(data["points"]);
      }
    });
  }

function create_comment(){
  var mod_id = $("#page_info").attr("mod_pk");
  var proj_id = $("#page_info").attr("proj_pk");
  var current_url = "/"+proj_id+"/"+mod_id+"/";
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
  var mod_id = $("#page_info").attr("mod_pk");
  var proj_id = $("#page_info").attr("proj_pk");
  var current_url = "/"+proj_id+"/"+mod_id+"/";
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
  var proj_id = $("#page_info").attr("proj_pk");
  var get_next = "/"+proj_id+"/"+"next/" + id + "/"
  $.ajax({
    type: "GET",
    url: get_next,
    success: function(data){
      var proj = data['proj_pk'];
      var mod = data['mod_pk'];
      if(proj == '-1'){
        console.log("wow");
        window.location.href = '/email/';
      } else{
        var mod_url = "/"+proj+"/"+mod + "/";
        $("#mod_bar_wrap").load(mod_url+ " .module_bar");
        $("#com_wrap").load(mod_url + " .comments");
        $("#section_wrap").load(mod_url + " .sections");
        $("#auth_title").load(mod_url + " .change_mod");
        $("#ppoints").load(mod_url + " #ppoints");
        if(String(proj_id) != String(data['proj_pk'])){
          console.log(proj_id);
          console.log(proj);
          $("#upvote_load").load(mod_url + " #upvote_load");
        }
        history.pushState(null,null, mod_url);
      }
    }
  });
}

function get_prev_mod(id){
  var proj_id = $("#page_info").attr("proj_pk");
  var get_prev = "/"+proj_id+"/"+"prev/" + id + "/"
  $.ajax({
    type: "GET",
    url: get_prev,
    success: function(data){
      var mod_url = "/"+data['proj_pk']+"/"+data['mod_pk'] + "/";
      $("#mod_bar_wrap").load(mod_url+ " .module_bar");
      $("#com_wrap").load(mod_url + " .comments");
      $("#section_wrap").load(mod_url + " .sections");
      $("#auth_title").load(mod_url + " .change_mod");
      $("#ppoints").load(mod_url + " #ppoints");
      if(String(proj_id) != String(data['proj_pk'])){
        $("#upvote_load").load(mod_url + " #upvote_load");
      }

      history.pushState(null,null, mod_url);
    }
  });
}


function handlersOff(){
  $(".comment_down, .comment_up, .post_up").off("click");
  $(".comment_text, .expand_wrap").off("click");
  $(".reply_wrap").off("click");
  $("#comment_form").off("submit");
  $(".comment_up, .comment_down, .glyphicon-menu-right, .glyphicon-menu-left, .post_up").off("mouseenter mouseleave");
}

//go left, comments
