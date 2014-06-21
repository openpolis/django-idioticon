=====
Usage
=====

Using bootstrap (with pophover plugin) we can build a tooltip system.

First create a template for terms in `idioticon/term_pophover.html`::

    <a href="#" rel="info-popover" data-toggle="popover"
       title="{{ term.get_name|safe|force_escape }}"
       data-content="{{ term.get_definition|safe|force_escape }}"
       data-html="true"
       data-width="300px"
       data-container="body"
       data-placement="auto">{{ term.get_name }}</a>

Then in your templates::

    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">

    ...

    {% load idioticon %}
    {% term_tag 'my-term' theme='pophover' %}

    ...

    <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.js"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
    <script>
    $(document).ready(function(){
        // activate popover
        $('a[rel=info-popover]').popover();
    });
    </script>

