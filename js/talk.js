require(["wq/app", "config", "templates", "slides"],
function(app, config, templates) {
var baseurl = window.location.pathname.replace(/\/$/, "");
app.init(config, templates, baseurl);
});
