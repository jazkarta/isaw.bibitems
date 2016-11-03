jQuery(function () {

  var $bib_uri_input = $('input#form-widgets-bibliographic_uri, input#form-widgets-IBibliographicItem-bibliographic_uri');
  if ($bib_uri_input.length){
    var $lookup = $('<button class="BibInfoFetchButton" title="Fetch bibliographic data"><span>Fetch Bib Info</span></button>');
    $bib_uri_input.after($lookup);
    $lookup.on('click submit', function (ev) {
      var uri = $bib_uri_input.val();
      ev.preventDefault();
      ev.stopPropagation();
      if (uri) {
        var p_url = portal_url[portal_url.length - 1] != '/' ? portal_url : portal_url.substring(0, portal_url.length - 1)
        var fetch_url = p_url + '/@@fetch-bibliographic-data';
        $.getJSON(
          fetch_url,
          {"url": uri},
          function (data) {
            if (data.error) {
              window.alert(data.error);
              return;
            }
            var $short_title = $bib_uri_input.parents().find('#form-widgets-short_title');
            var $full_title = $bib_uri_input.parents().find('#form-widgets-title, #form-widgets-IBibliographicItem-title');
            var $description = $bib_uri_input.parents().find('#form-widgets-description, #form-widgets-IBibliographicItem-description');
            var $detail = $bib_uri_input.parents().find('#form-widgets-citation_detail, #form-widgets-IBibliographicItem-citation_detail');
            var $formatted = $bib_uri_input.parents().find('#form-widgets-formatted_citation, #form-widgets-IBibliographicItem-formatted_citation');
            var $access_uri = $bib_uri_input.parents().find('#form-widgets-access_uri, #form-widgets-IBibliographicItem-access_uri');
            var title = data.short_title || data.title;
            if ($short_title.length) {
              $short_title.val(data.short_title || '');
              if (data.title && $full_title.length) {
                $full_title.val(data.title);
              }
            } else if (title && $full_title.length) {
              $full_title.val(title);
            }
            if (data.citation_detail) {
              $detail.val(data.citation_detail);
            }
            if (data.formatted_citation) {
              $formatted.val(data.formatted_citation);
            }
            if (data.access_uri) {
              $access_uri.val(data.access_uri);
            }
            if (data.bibliographic_uri) {
              $bib_uri_input.val(data.bibliographic_uri);
            }
            if (data.plain) {
              $description.val(data.plain);
            }
          }
        ).error(function (resp) {
            try {
              var data = JSON.parse(resp.responseText);
              window.alert(data.error);
            } catch(err) {
              window.alert('Error code: ' + resp.status + ' while retrieving Zotero response');
            }
        });
      }
      return false;
    });
  }
});
