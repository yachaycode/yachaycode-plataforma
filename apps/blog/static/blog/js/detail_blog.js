 /*Js datlle de blog*/
  $.ajaxSetup({
       beforeSend: function(xhr, settings) {
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
           if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
               // Only send the token to relative URLs i.e. locally.
               xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
           }
       }
  });
  $( document ).ready(function() {
    $.ajax( {
        type: "POST",
        url: '/blog/contador-visitas-ajax/',
        data: {'id': $('#id_blog').val()},
        success: function( data ) {
          var resultado = JSON.parse(data);
          if (!resultado.status) {
             alert("Error de server: " + resultado.error)
             return false 
          }
        },
          error : function() {
           alert('Disculpa, error del servidor o opción no válida..!');
       }

      } );
  });
