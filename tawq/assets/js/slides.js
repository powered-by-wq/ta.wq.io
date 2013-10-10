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

var slides, dskey = {'url': ''};

// Connect markdown processor to code highlighter
marked.setOptions({
    'highlight': function(code, lang) {
        return highlight.highlight(lang, code).value;
    }
});

// Collect, sort, attach events to and return slides
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
    // This makes it possible to use jQuery deep extend to combine various 
    // formats into a single configuration object.
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
        // Define an index.yml or index.json with an order attribute...
        order = items.index.order;
    else
        // ... or we'll just use dictionary key order
        order = Object.keys(items);

    order.forEach(function(name) {
        if (!items[name]) {
            if (window.console)
                console.warn('Slide ' + name + ' is not defined!');
            return;
        }
        if (items[name].index) {
            // Nested object; recursively add children to end of array
            result = result.concat(sort(items[name], prefix + name + "."));
        } else {
            // Not nested, give object a unique ID and a pointer to its parent
            items[name].id = prefix + name;
            items[name].parent = items;
            result.push(items[name]);
        }
    });

    // Nested object, return to parent
    if (prefix)
        return result;

    // Add navigation links to final array
    result.forEach(function(name, i) {
        var slide = result[i];
        slide.number = i + 1; // index
        if (i > 0)
            slide.prev = result[i - 1].id;
        if (i < result.length - 1) {
            var next = result[i + 1];
            slide.next = next.id;
            if (next.transition)
                slide.next_transition = next.transition;
        }
    });
    return result;
}

// Run custom JS for a slide when it is shown.  
function onShow(match, ui, params, hash, evt, $page) {
    var slide = ds.find(dskey, match[1]);
    if (!slide)
        return;
    if (slide.js) {
        // The custom JS should be in an AMD module with a run() function.
        // For optimal speed, preload the module by require-ing it in custom.js
        var modname = (slide.js === true ? match[1] : slide.js);
        require(['assets/' + modname], function(mod) {
            if (slide.delay)
                setTimeout(run, slide.delay * 1000);
            else
                run();
            function run() {
                mod.run(slide, $page);
            }
        });
    }   
}

// Context helpers for Mustache templates (see templates/ for uses)
function context() {

    return {
        // Copy of slide list for use by menu
        'slides': function(){ return slides.array },

        'count': function(){ return slides.array.length },

        // Is this slide the current one? (for menu rendering)
        'current': function() {
            return this.id == pages.info.prev_path;
        },

        // Is this slide before the current one (for reverse transition)
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
        },

        // If the context has a "two-column" attribute, load the second column
        // (must be a sibling of the current slide)
        'split': function() {
            if (!this['two-column'] || !this.parent)
                return false;
            return this.parent[this['two-column']];
        },

        // Flip transition - don't used fixed header / footer
        'flip': function() {
            return this.transition == 'flip';
        },

        // Use "down" arrow when next slide is going to come up from bottom
        'next_down': function() {
            return this.next_transition == 'slideup';
        },

        // Use "up" arrow for previous slide as this slide came up from bottom 
        // (named "down" for consistency w/above)
        'down': function() {
            return this.transition == 'slideup';
        }
    }
}

});
