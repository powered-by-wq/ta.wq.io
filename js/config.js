// Configuration for wq/app.js
define(["wq/lib/marked", "wq/pages", "slides"],
function (marked, pages, slides) {
return {
   // app.js router configuration
   'pages': {
       'slide': {'url': '', 'list': true},
       'menu': {'url': 'menu'}
   },

   // jQuery Mobile transitions
   'transitions': {
      'default': 'slide',
      'maxwidth': false
   },

   // template defaults
   'defaults': {
       // Copy of slide list for use by menu
       'slides': slides.array, 

       // Content for menu labels & HTML <title>
       'label': function() {
           return this.title || this.id;
       },
       
       // If the context includes a "markdown" attribute, render it as HTML
       'html': function() {
           if (!this.markdown)
               return "";
           return marked.parse(this.markdown);
       }
   }
};
});
