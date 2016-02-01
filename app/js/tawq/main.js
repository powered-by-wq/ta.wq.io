define(['wq/app', 'wq/map', 'wq/markdown', 'wq/photos', 'wq/template', 'wq/router',
        './toolbars', './resize', './config',
        'leaflet.draw'],
function(app, map, md, photos, tmpl, router, toolbars, resize, config) {

app.use(map);
app.use(photos);
app.use(toolbars);
app.use(resize);

config.presync = presync;
config.postsync = postsync;
app.init(config).then(function() {
    tmpl.setDefault('html', function() {
        var parts = this.markdown_parts;
        var markdown;
        if (parts) {
            var step = router.info.params && parseInt(router.info.params.step) || 0;
            if (step >= parts.length) {
                step = parts.length - 1;
            }
            markdown = parts.slice(0, step + 1).join('\r\n');
        } else {
            markdown = this.markdown;
        }
        return md.parse(markdown);
    });
    app.jqmInit();
    app.models.slide.load().then(function(slides) {
        config.slides = slides.list;
    });
    app.prefetchAll();
});

// Sync UI
function presync() {
    $('button.sync').html("Syncing...");
    $('li a.ui-icon-minus, li a.ui-icon-alert')
       .removeClass('ui-icon-minus')
       .removeClass('ui-icon-alert')
       .addClass('ui-icon-refresh');
}

function postsync(items) {
    $('button.sync').html("Sync Now");
    app.syncRefresh(items);
}

});
