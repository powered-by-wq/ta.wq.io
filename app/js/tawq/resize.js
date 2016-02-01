define(['wq/app', 'wq/markdown', 'wq/outbox', 'jquery.mobile'], function(app, md, outbox, jqm) {
return {
    'name': 'resize',
    'init': function() {
    },
    'run': function(page, mode, itemid, url) {
        if (page != 'slide' || mode != 'detail') {
            return;
        }
        var $div = jqm.activePage.find('[role=main]');
        if ($div.data('lock-zoom')) return;
        app.models.slide.find(itemid).then(function(slide) {
        if (slide.markdown_parts) {
            var n = slide.markdown_parts.length - 1;
            if (url.indexOf('step=' + n) == -1) {
                return;
            }
        } else if (slide.image) {
            var left, top;
            var $img = $div.find('img');
            if ($img[0].complete) {
               loadImg();
            } else {
               $img.on('load', loadImg);
            }
            function loadImg() {
            if (slide.image_mode == 'height') {
                left = window.innerWidth / 2 - $img.width() / 2;
                $img.css('left', left + 'px');
                if (app.user && Math.round(left * 100) != Math.round(slide.left * 100)) {
                    $.post('/slides/' + itemid + '/zoom.json', {
                       'left': left,
                       'top': 0,
                       'csrfmiddlewaretoken': outbox.csrftoken
                    });
                }
            } else {
                top = window.innerHeight / 2 - $img.height() / 2;
                $img.css('top', top + 'px');
                if (app.user && Math.round(top * 100) != Math.round(slide.top * 100)) {
                    $.post('/slides/' + itemid + '/zoom.json', {
                       'top': top,
                       'left': 0,
                       'csrfmiddlewaretoken': outbox.csrftoken
                    });
                }
            }
            }
            return;
        } else if (!slide.markdown) {
            return;
        }
        var zoom = slide.zoom;
        var startZoom = zoom;
        var height = window.innerHeight - 120;
        var width = window.innerWidth - 20;
        /*
        while (jqm.activePage.height() > height*zoom && zoom > 0.5) {
            zoom -= 0.1;
            //$div.css('zoom', zoom);
            $div.css('-webkit-transform', 'scale(' + zoom + ')');
        }
        while (jqm.activePage.height() <= height*zoom && zoom < 10) {
            zoom += 0.1;
            //$div.css('zoom', zoom);
            $div.css('-webkit-transform', 'scale(' + zoom + ')');
        }
        */
        zoom = height / $div.height();
        if (zoom > 8) {
             zoom = 8;
        }
        $div.width(width / zoom);
        while ($div.height() * zoom > height && zoom > 1.0) {
            zoom -= 0.1;
            $div.width(width / zoom);
        }
        $div.width(width / zoom);
        $div.css('-webkit-transform', 'scale(' + zoom + ')');
        if (app.user && Math.round(zoom * 100) != Math.round(startZoom * 100)) {
            $.post('/slides/' + itemid + '/zoom.json', {
               'zoom': zoom,
               'width': width / zoom,
               'csrfmiddlewaretoken': outbox.csrftoken
            });
        }
        });
    }
};
});
