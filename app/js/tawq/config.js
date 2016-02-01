define(["data/config", "data/templates", "data/version"],
function(config, templates, version) {

config.router = {
    'base_url': ''
}

config.template = {
    'templates': templates,
    'defaults': {
        'version': version,
        'presentation_id': function() {
             return window.TAWQ_PRESENTATION || config.slides && config.slides[0].presentation_id;
        },
        'slides': function() {
             var slides = (config.slides || []).filter(function(slide) {
                 if (window.TAWQ_PRESENTATION==slide.presentation_id) {
                     return true;
                 }
             });
             var lastSection;
             var seen = false; 
             var parts = $.mobile.activePage.jqmData('url').split('/');
             var slug = parts[parts.length - 1];
             slides.forEach(function(slide) {
                 if (slide.section_id != lastSection) {
                     slide.new_section = true;
                     lastSection = slide.section_id;
                 }
                 if (slide.id == slug) {
                     slide.current = true;
                     seen = true;
                 } else {
                     slide.current = false;
                     slide.reverse = !seen;
                 }
             });
             return slides;
        }
    }
};

config.store = {
    'service': config.router.base_url,
    'defaults': {'format': 'json'}
}

config.map = {
    'bounds': [[44.7, -93.6], [45.2, -92.8]]
};

config.outbox = {};
config.noBackgroundSync = true;

config.transitions = {
    'default': "none",
    'save': "none",
    'maxwidth': 100000
};

return config;

});
