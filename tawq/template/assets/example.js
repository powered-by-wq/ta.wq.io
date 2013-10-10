define(['data'],
function(data) {

var example = {};

example.run = function(conf, $slide) {
    $slide.find('.ui-content').html(
        "Data: " + data.example[0].name
    );
}

return example;

});
