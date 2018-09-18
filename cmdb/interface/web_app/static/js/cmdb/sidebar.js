
(function($, global, undefined) {
  'use strict';
  $.fn.sidebar = function(opt) {

    $(this).on('click', function(e) {
      e.preventDefault();

      if(document.cookie.indexOf('sidebar_hidden') == -1){
        document.cookie='sidebar_hidden=1; path=/';
      } else {
        document.cookie='sidebar_hidden=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
      }
      $('body').toggleClass('sidebar-hidden');
    });

  }

  if (global.module && global.module.exports) {
    module.exports = $.fn.sidebar;
  }
})(jQuery, window || global);
