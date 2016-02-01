define(['wq/app', 'jquery.mobile'], function(app, jqm) {
return {
    'name': 'toolbars',
    'init': function() {
         this.$header = $("[data-role='header']").toolbar();
         this.$footer = $("[data-role='footer']").toolbar();
         this.$previous = this.$footer.find('a:first-child');
         this.$flip = this.$header.find('button');
         this.$next = this.$footer.find('a:last-child');
         this.nextImg = new Image();
         this.previousImg = new Image();
         this.$flip.click(function() {
             $.mobile.activePage.find('iframe').toggleClass('mobile');
         });
    },
    'run': function(page, mode, itemid, url) {
        var self = this;
        if (page != 'slide' || mode != 'detail') {
            self.$header.fadeOut();
            self.$footer.fadeOut();
            return;
        }
        var match = url.match(/step=(\d+)/);
        var step = match && parseInt(match[1]) || 0;
        app.models.slide.find(itemid).then(function(slide) {
            var lastStep = slide.markdown_parts ? slide.markdown_parts.length - 1 : 0;
            if (slide.title) {
                self.$header.find('h1').text(slide.title);
                self.$header.fadeIn();
            } else {
                self.$header.fadeOut();
            }
            if (slide.url) {
                self.$footer.find('h3').text(slide.url);
                self.$flip.show();
            } else {
                self.$footer.find('h3').text('@wq_framework');
                self.$flip.hide();
            }
            var showFooter = false;
            if (step < lastStep) {
                slideLink(self.$next, {
                    'id': itemid + '?step=' + (step+1),
                    'icon': 'carat-r',
                    'transition': 'none'
                });
                showFooter = true;
            } else {
                if (slide.next) {
                    slideLink(self.$next, slide.next);
                    if (slide.next.image) {
                        self.nextImg.src = slide.next.image;
                    }
                    showFooter = true;
                } else {
                    self.$next.hide();
                }
            }
            if (step > 0) {
                slideLink(self.$previous, {
                    'id': itemid + '?step=' + (step-1),
                    'icon': 'carat-l',
                    'transition': 'none'
                });
                showFooter = true;
            } else {
                if (slide.previous) {
                    slideLink(self.$previous, slide.previous);
                    if (slide.previous.image) {
                        self.previousImg.src = slide.previous.image;
                    }
                    showFooter = true;
                } else {
                    self.$previous.hide();
                }
            }
            if (showFooter)
                self.$footer.fadeIn();
            else
                self.$footer.fadeOut();
        });

        function slideLink($link, attrs) {
            $link.attr('href', '/slides/' + attrs.id);
            if ($link[0].className) {
            $link[0].className.split(' ').forEach(function(cls) {
                if (cls.indexOf('ui-icon-') === 0) {
                    $link.removeClass(cls);
                }
            });
            }
            $link.addClass('ui-icon-' + attrs.icon);
            $link.jqmData('transition', attrs.transition);
            if (attrs.transition == 'flow' || attrs.transition == 'flip') {
                $link.on('click.flow', function() {
                    self.$header.hide();
                    self.$footer.hide();
                });
            } else {
                $link.off('click.flow');
            }
            $link.show();
        }
    }
};
});
