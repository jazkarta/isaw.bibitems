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
            var $parents = $bib_uri_input.parents();
            var $short_title = $parents.find('#form-widgets-short_title');
            var $full_title = $parents.find('#form-widgets-title, #form-widgets-IBibliographicItem-title');
            var $description = $parents.find('#form-widgets-description, #form-widgets-IBibliographicItem-description');
            var $detail = $parents.find('#form-widgets-citation_detail, #form-widgets-IBibliographicItem-citation_detail');
            var $formatted = $parents.find('#form-widgets-formatted_citation, #form-widgets-IBibliographicItem-formatted_citation');
            var $access_uri = $parents.find('#form-widgets-access_uri, #form-widgets-access_uris, #form-widgets-IBibliographicItem-access_uri');
            var $authors = $parents.find('#form-widgets-authors');
            var $editors = $parents.find('#form-widgets-editors');
            var $contributors = $parents.find('#form-widgets-contributors');
            var $publisher = $parents.find('#form-widgets-publisher');
            var $isbn = $parents.find('#form-widgets-isbn');
            var $issn = $parents.find('#form-widgets-issn');
            var $doi = $parents.find('#form-widgets-doi');
            var $date_of_publication = $parents.find('#form-widgets-date_of_publication');
            var $text = $parents.find('#form-widgets-text');
            var $parent_title = $parents.find('#form-widgets-parent_title');
            var $volume = $parents.find('#form-widgets-volume');
            var $range = $parents.find('#form-widgets-range');
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
              if ($access_uri.is('textarea') && $access_uri.val() && $access_uri.val() != data.access_uri) {
                if ($access_uri.val().split('\n')[0] != data.access_uri) {
                  $access_uri.val(data.access_uri + '\n' +  $access_uri.val());
                }
              } else {
                $access_uri.val(data.access_uri);
              }
            }
            if (data.bibliographic_uri) {
              $bib_uri_input.val(data.bibliographic_uri);
            }
            if (data.plain) {
              $description.val(data.plain);
            }
            if (data.authors) {
              $authors.val(data.authors.map(function (m) {return m.name || (m.firstName + ' ' + m.lastName);}).join("\n"));
            }
            if (data.editors) {
              $editors.val(data.editors.map(function (m) {return m.name || (m.firstName + ' ' + m.lastName);}).join("\n"));
            }
            if (data.contributors) {
              $contributors.val(data.contributors.map(function (m) {return m.name || (m.firstName + ' ' + m.lastName);}).join("\n"));
            }
            if (data.publisher) {
              $publisher.val(data.publisher);
            }
            if (data.isbn) {
              $isbn.val(data.isbn);
            }
            if (data.issn) {
              $issn.val(data.issn);
            }
            if (data.doi) {
              $doi.val(data.doi);
            }
            if (data.date_of_publication) {
              $date_of_publication.val(data.date_of_publication);
            }
            if (data.parent_title) {
              $parent_title.val(data.parent_title);
            }
            if (data.volume) {
              $volume.val(data.volume);
            }
            if (data.range) {
              $range.val(data.range);
            }
            if (data.text) {
              $text.val(data.text);
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
