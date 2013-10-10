require.config({'paths': {'assets': '../assets'}});

require(["wq/app", "config", "templates", "slides", "custom"],
function(app, config, templates, slides) {
var baseurl = window.location.pathname.replace(/\/$/, "");
app.init(config, templates, baseurl);
slides.init();
});
