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

  $("#updated").on("submit", "#email_form", function(e){
    e.preventDefault();
    send();
  });

  $("#email_submit").hover(function(){
    $(this).css("background-color", "rgb(80, 204, 127)");
  }, function(){
    $(this).css("background-color", "#eee");
  });

});

function send(){
  var new_email = $('#email_field').val();
  if( new_email.indexOf("@") >= 0 && new_email.indexOf(".") >= 0){
    $.ajax({
      type: "POST",
      url: "/email/",
      data: {
        'new_email': new_email,
      },
      success: function(){
        document.getElementById("updated").innerHTML = "<h1 id='thank'>Thank You</h1>";
      }
    });
  } else {
    alert("Please enter a valid email");
  }
}
