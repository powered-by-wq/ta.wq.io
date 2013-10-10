tawq
====

Write presentations in YAML & Markdown; deploy them as a jQuery Mobile
HTML5 app. Powered by `wq.app <http://wq.io/wq.app>`_ modules
and `the modules wq.app is powered
by <http://wq.io/docs/third-party>`_.

Examples
--------

See http://ta.wq.io.

Getting Started
---------------

::

    pip install tawq
    tawq start my-presentation && cd my-presentation
    tawq build

Slide Configuration
-------------------

Each slide is defined by JSON, YAML, Markdown, and/or HTML, each of
which should be created as separate files under slides/. Use .json,
.yml, .md, and .html as extensions for each of the formats,
respectively. Use subfolders to group related slides. If you define both
a YAML and a JSON configuration for the same slide, the YAML will be
used (after being converted to JSON). If you define both Markdown and
HTML, the HTML will be used.

Each slide configuration can define the following attributes:

Navigation options
~~~~~~~~~~~~~~~~~~

-  **title** - Title for the slide, to be displayed at the top of the
   slide and in the menu. Leave blank to use the space for slide
   content.
-  **label** - Label for this slide in the menu (if different than
   title, or if title is blank).
-  **section** - Text for a section header which will be added in the
   menu right before this slide.
-  **transition** - Transition to use when opening slide. Should be one
   of `jQuery Mobile's
   options <http://view.jquerymobile.com/1.3.2/dist/demos/widgets/transitions/>`_.
-  **menu-hide** - Don't show the slide in the menu, useful if slide is
   a continuation of a previous one. Often used with
   ``transition: "none"``.

Basic Content options
~~~~~~~~~~~~~~~~~~~~~

One (and only one) of the following should be defined:

-  **markdown** - Markdown to be rendered into HTML and used as the
   slide content. This can be defined in a separate .md file with the same name.
-  **html** - Raw HTML to be used as the slide content. This can be defined
   in a separate .html file with the same name.
-  **url** - A URL to an external page to use as the slide content (via
   an ``<iframe>``). The url will be desplayed at the bottom of the
   slide.
-  **image** - An image to display at full height (default) or full width.
-  **bullets** - A list of bullet points (defined as an array) to use as
   the slide content. It's usually more flexible to use markdown for
   this. (Also, slides full of bullet points are boring)

Advanced content options
~~~~~~~~~~~~~~~~~~~~~~~~

-  **hide-url** - Set to true to turn off the url display.
-  **image-wide** - Set to true to use full width mode for the image
-  **two-column** - Split the slide into two blocks. The value of this
   should be the name of a second configuration file containing
   content/html to place in the second block.
-  **class** - CSS class to apply to the slide container div

Scripting options
~~~~~~~~~~~~~~~~~

-  **js** - the name of an AMD module to execute when the file is shown.
   The module should define a ``run()`` function for this purpose. The
   ``run`` function will be called with the slide configuration as the
   argument. The js file should be stored in ``assets``.
-  **delay** - Seconds to wait before executing the script

Ordering
~~~~~~~~

Rather than ordering alphabetically, every folder (including the root)
should have an index.yml or index.json. This file can also be used as a
normal slide, but should have an additional **order** attribute listing
all of the other slides in your preferred order. If the order attribute
does not list the index itself it will not be included. If you do not
add an order attribute, the slides will be ordered by whatever
Objects.keys() decides is a good order for the compiled dictionary.

Each of these rules is totally arbitrary and most/all can be overridden
by changing the application code.

Building the Presentation
-------------------------

Use ``tawq build``.
