// Configuration for wq/app.js
define(["./slides"],
function (slides) {
return {
   // app.js router configuration
   'pages': {
       'slide': {'url': '', 'list': true},
       'menu': {'url': 'menu'}
   },

   // jQuery Mobile transitions
   'transitions': {
      'default': 'slide',
      'maxwidth': 10000
   },

   // template defaults
   'defaults': slides.context
}
});
