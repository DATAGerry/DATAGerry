/*
 * Error error_code
 * based on https://codepen.io/Ahmed_B_Hameed/pen/LkqNmp
 */

(function($, global, undefined) {
  'use strict';

  $.error_code = {
    defaults: {
			thirdDigit: 4,
      secondDigit: 0,
      firstDigit: 4
    }
  };

  $.fn.error_code = function(opt) {
    var code = $.extend({}, $.error_code.defaults, opt);
    var error_target = this;
    this.randomNum = function() {
      "use strict";
      return Math.floor(Math.random() * 9) + 1;
    }

    var loop1, loop2, loop3, time = 30,
      i = 0,
      number;
    var selector3 = $('.thirdDigit',this);
    var selector2 = $('.secondDigit',this);
    var selector1 = $('.firstDigit',this);

    this.loop3 = setInterval(function() {
      "use strict";
      if (i > 40) {
        clearInterval(loop3);
        selector3.text(code.thirdDigit);
      } else {
        selector3.text(error_target.randomNum());
        i++;
      }
    }, time);
    this.loop2 = setInterval(function() {
      "use strict";
      if (i > 80) {
        clearInterval(loop2);
        selector2.text(code.secondDigit);
      } else {
        selector2.text(error_target.randomNum());
        i++;
      }
    }, time);
    this.loop1 = setInterval(function() {
      "use strict";
      if (i > 100) {
        clearInterval(loop1);
        selector1.text(code.firstDigit);
      } else {
        selector1.text(error_target.randomNum());
        i++;
      }
    }, time);

  };

  if (global.module && global.module.exports) {
    module.exports = $.fn.error_code;
  }
})(jQuery, window || global);
