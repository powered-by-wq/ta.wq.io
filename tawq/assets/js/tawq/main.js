define(["wq/app", "wq/markdown",
       "./config", "./templates", "./slides", "./custom"],
function(app, markdown, config, templates, slides) {
var baseurl = window.location.pathname.replace(/\/$/, "");
app.init(config, templates, baseurl);
markdown.init();
slides.init();
});
