/*!
 * tawq - slides.js
 * Organizes collected configuration & markup into an interlinked slide deck.
 * (c) 2013 S. Andrew Sheppard
 * http://wq.io/license
 * http://ta.wq.io
 */

define(["wq/lib/jquery", "wq/lib/marked", "wq/lib/highlight",
        "wq/pages", "wq/store", 
        "slides/json", "slides/yaml", "slides/html", "slides/markdown"],
function($, marked, highlight, pages, ds, json, yaml, html, markdown) {

marked.setOptions({
    'highlight': function(code, lang) {
        return highlight.highlight(lang, code).value;
    }
});

var slides, dskey = {'url': ''};

makeObjects(html, "html");
makeObjects(markdown, "markdown");
slides = $.extend(true, {}, json, yaml, html, markdown);
slides.array = sort(slides, "");
slides.context = context();
slides.init = function() {
    pages.addRoute('(.+)', 's', onShow);
};
ds.set(dskey, slides.array, true);

return slides;

function makeObjects(items, key) {
    // Convert e.g {'key1': '<html>'} to {'key1': {'html': '<html>'}}
    var name;
    for (name in items) {
        if (typeof items[name] == "string") {
            var obj = {};
            obj[key] = items[name];
            items[name] = obj;
        } else {
            makeObjects(items[name], key);
        }
    }
}

function sort(items, prefix) {
    // Flatten object values to array, recursively if needed
    var result = [], name, i, order;
    if (items.index && items.index.order)
        order = items.index.order;
    else
        order = Object.keys(items);

    order.forEach(function(name) {
        if (items[name].index) {
            // Nested object
            result = result.concat(sort(items[name], name + "."));
        } else {
            items[name].id = prefix + name;
            result.push(items[name]);
        }
    });

    // Nested object, return to parent
    if (prefix)
        return result;

    // Add navigation links to final array
    result.forEach(function(name, i) {
        result[i].number = i + 1;
        if (i > 0)
            result[i].prev = result[i - 1].id;
        if (i < result.length - 1)
            result[i].next = result[i + 1].id;
    });
    return result;
}

function onShow(etype, match, ui, page, evt) {
    var slide = ds.find(dskey, match[1]);
    if (!slide)
        return;
    if (slide.js) {
        var modname = (slide.js === true ? match[1] : slide.js);
        require([modname], function(mod) {
            mod.run(slide);
        });
    }   
}

function context() {
    return {
        // Copy of slide list for use by menu
        'slides': function(){ return slides.array },

        'count': function(){ return slides.array.length },

        // Navigation helpers
        'current': function() {
            return this.id == pages.info.prev_path;
        },

        'before': function() {
            var current = ds.find(dskey, pages.info.prev_path); 
            if (current)
                return this.number < current.number;
        },

        'after': function() {
            var current = ds.find(dskey, pages.info.prev_path); 
            if (current)
                return this.number > current.number;
        },

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
}

});
