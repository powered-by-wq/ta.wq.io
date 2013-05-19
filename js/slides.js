/*!
 * tawq - slides.js
 * Organizes collected configuration & markup into an interlinked slide deck.
 * (c) 2013 S. Andrew Sheppard
 * http://wq.io/license
 * http://ta.wq.io
 */

define(["wq/lib/jquery", "wq/store", 
        "slides/json", "slides/yaml", "slides/html", "slides/markdown"],
function($, ds, json, yaml, html, markdown) {

var slides;

makeObjects(html, "html");
makeObjects(markdown, "markdown");
slides = $.extend(true, {}, json, yaml, html, markdown);
slides.array = sort(slides, "");
ds.set({'url':''}, slides.array, true);

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
        if (i > 0)
            result[i].prev = result[i - 1].id;
        if (i < result.length - 1)
            result[i].next = result[i + 1].id;
    });
    return result;
}

});
