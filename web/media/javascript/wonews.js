// Winter's Oasis Javascript library
// Copyright 2012 Kelketek Enterprises LLC
// http://www.kelketek.com
var resizer = function () {
    var FOOTER_HEIGHT = 70;
    var elem = $('body');
    if ( $(window).height() >= $(document).height() )  {
        elem.css({'height' : $(window).height()});
    } else {
        elem.css({'height' : $(document).height()});
    }
}
$(document).load(resizer);
$(document).ready(resizer);
$(window).resize(resizer);

function footer_login (){
  document.loginform.value = 'login';
  document.loginform.submit();
}
