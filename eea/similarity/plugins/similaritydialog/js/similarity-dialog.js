function suggestions_dialog(){
    var portal_type = $('body').attr('class').match('portaltype-[a-z-]*');
    var portal_type_length;
    if (portal_type) {
        portal_type = portal_type[0].split('-');
        portal_type_length = portal_type.length;
        portal_type = portal_type_length === 2 ? portal_type[1] :
            portal_type[1] + portal_type[2];
    }
    var title = $('#title').val();
    $('#similarity-dialog').remove();
    var base_url = (jQuery('body').data('base-url') || jQuery("base").attr("href") || "").split('portal_factory')[0];
    var get_suggestions_url = (base_url.endsWith('/') ?
        base_url + 'get_suggestions': base_url + '/get_suggestions');
    var suggestions = $.get(
        get_suggestions_url,
        {'portal_type': portal_type, 'title': title},
        function(data){
            $.suggestionsDialog({
                'suggestions': data
            });
        },
        'json');
}

$(function() {
    $.suggestionsDialog = function(options) {
      var dialog_title = 'Please check these possible duplicates:';
      var dialog_title_no_suggestions = 'Please check these possible duplicates:';
      var dialog_text = 'We have found a list of possible duplicates based on your title choice:';
      var dialog_text_no_suggestions = 'There are no suggestions for duplicate content based on the title';
      var base_url = (jQuery('body').data('base-url') || jQuery("base").attr("href") || "").split('portal_factory')[0];
      var get_suggestions_text_url = (base_url.endsWith('/') ?
          base_url + 'get_suggestions_text': base_url + '/get_suggestions_text');
      var text_data = $.ajax({
          url: get_suggestions_text_url,
          type: 'get',
          async: false,
          dataType: 'json',
          success: function(data){
              if (data[0]){
                  dialog_title = data[0];
              }
              if (data[1]){
                  dialog_text = data[1];
              }
               if (data[2]){
                  dialog_title_no_suggestions = data[2];
              }
              if (data[3]){
                  dialog_text_no_suggestions = data[3];
              }
          }
      });
      var settings = {
        dialog_title : dialog_title,
        dialog_text: dialog_text,
        dialog_title_no_suggestions : dialog_title_no_suggestions,
        dialog_text_no_suggestions: dialog_text_no_suggestions,
        counter: 0,
        dialog_width: 383
      };

      $.extend(settings, options);

      var SuggestionsDialog = {
        setupDialog: function() {
          var self = this;
          self.destroyDialog();

          var suggestions = Object.keys(options.suggestions).length;
          var current_title;
          var current_text;

          if (suggestions){
              current_title = settings.dialog_title;
              current_text = settings.dialog_text;
          } else {
              current_title = settings.dialog_title_no_suggestions;
              current_text = settings.dialog_text_no_suggestions;
          }
          var list = $('<ul/>');
          $.each(settings.suggestions, function(url, sugg){
              list.append($('<li/>')
                  .append(
                      $('<a/>')
                          .attr('title', 'Similarity score: ' + sugg[4])
                          .attr('href', url).append(sugg[0])
                  )
                  .append($('<span>').attr('class', 'suggestion-details')
                      .append(' (similarity score: ' + sugg[4] + ')')
                  )
                  .append($('<div/>')
                      .attr('class', 'suggestion-details')
                       .append($('<span>')
                          .attr('class', 'portalType').text(sugg[1]))
                      .append($('<span>').attr('class', 'docDate creationDate')
                          .append(
                              $('<span>').attr('class', 'byline-separator')
                          )
                          .append('Created ' + sugg[2])
                      )
                      .append($('<span>').attr('class', 'docDate publishDate')
                          .append(
                              $('<span>').attr('class', 'byline-separator')
                          )
                          .append('Published ' + sugg[3])
                      )
                  )
              );
          });
          var html = $('<div/>').attr('id', 'similarity-dialog')
                           .append($('<p/>').attr('id', 'similarity-text')
                              .append(current_text)
                          );
          html.append(list)
          .appendTo('body')
          .dialog({
            modal: false,
            width: settings.dialog_width,
            minHeight: 'auto',
            zIndex: 10000,
            closeOnEscape: true,
            draggable: false,
            resizable: false,
            dialogClass: 'similarity-dialog',
            title: current_title,
            show: {
                    effect: "fade",
                    duration: 1000
                  },
            position: { my: "right top", at: "right bottom", of: window }
          });

        },

        destroyDialog: function() {
          if ($("#similarity-dialog").length) {
            $(this).dialog("close");
            $('#similarity-dialog').remove();
          }
        }
      };

      SuggestionsDialog.setupDialog();
    };
    var title;
    $('body').on('focusin', '#title', function(){
      if(!$('#get-suggestions').length){
        $(this).parent().parent().parent().parent().parent().parent().css({
            'overflow': 'hidden'
        });
        $(this)
          .animate({width: '95%'}, 600)
          .parent().append(
            $('<a/>')
              .attr('id', 'get-suggestions')
              .attr('title', 'Get suggestions for similar items')
              .attr('href', '#')
              .text('\u2248')
              .css({
                'font-size': '26px',
                'position': 'absolute',
                'border': '1px solid #ccc',
                'width': '25px',
                'text-align': 'center',
                'border-left': 'none',
                'height': '35px',
                'line-height': '1',
                'border-top-right-radius': '5px',
                'border-bottom-right-radius': '5px',
                'display': 'none'
            })
            .append(
                $('<div>')
                    .text('Click to get suggestions for similar items')
                    .addClass('similarities-helper')
                    .css({
                        'padding': '.5rem',
                        'position': 'absolute',
                        'top': '-62px',
                        'right': '-15px',
                        'z-index': '9999',
                        'font-size': '12px',
                        'line-height': '1.2',
                        'width': '160px',
                        'background': 'white',
                        'box-shadow': '0px 0px 4px #ccc',
                        'border-radius': '5px'
                    })
                    .append(
                        $('<span>')
                            .text('\u25BC')
                            .css({
                              'content':'\u25BC',
                              'position':'absolute',
                              'left':'75%',
                              'width':'0',
                              'height':'0',
                              'color':'white',
                              'text-shadow':'0px 3px 2px #ccc',
                              'font-size':'2em',
                              'pointer-events':'none',
                              'top': '33px'
                            })
                    )
            )
          );
      }
      $('#get-suggestions').animate(
          {opacity: 'show'},
          {duration: 600,
           complete: function(){
              $('.similarities-helper').animate(
                  {opacity: 'show'},
                  {duration: 600,
                   complete: function(){
                      setTimeout(function(){
                          $('.similarities-helper').animate({opacity: 'hide'}, 600);
                      }, 5000);
                   }
                  }
              );
           }
          }
      );
//      $('#get-suggestions').animate({opacity: 'show'}, 600);
      title = $('#title').val();
    });
    $("head").append($('<style>.similarities-helper:after {content:\u25BC; position:absolute; left:45%; width:0; height:0; color:white; text-shadow:0px 2px 3px #aaa; font-size:2em; pointer-events:none}</style>'));
    $('#title')
      .parent().append(
        $('<a/>')
            .attr('id', 'get-suggestions')
            .attr('title', 'Get suggestions for similar items')
            .attr('href', '#')
            .text('\u2248')
            .css({
              'font-size': '26px',
              'position': 'absolute',
              'border': '1px solid #ccc',
              'width': '22px',
              'text-align': 'center',
              'border-left': 'none',
              'height': '32px',
              'line-height': '1',
              'border-top-right-radius': '5px',
              'border-bottom-right-radius': '5px',
              'display': 'none'
            })
            .append(
                $('<div>')
                    .text('Click to get suggestions for similar items')
                    .addClass('similarities-helper')
                    .css({
                        'padding': '.5rem',
                        'position': 'absolute',
                        'top': '-62px',
                        'right': '-67px',
                        'z-index': '9999',
                        'font-size': '12px',
                        'line-height': '1.2',
                        'width': '160px',
                        'background': 'white',
                        'box-shadow': '0px 0px 4px #ccc',
                        'border-radius': '5px',
                        'display': 'none'
                    })
                    .append(
                        $('<span>')
                            .text('\u25BC')
                            .css({
                              'content':'\u25BC',
                              'position':'absolute',
                              'left':'45%',
                              'width':'0',
                              'height':'0',
                              'color':'white',
                              'text-shadow':'0px 3px 2px #ccc',
                              'font-size':'2em',
                              'pointer-events':'none',
                              'top': '33px'
                            })
                    )

            )
      );
    setTimeout(function(){
        $('#title')
          .animate({width: '96%'}, 600);
        $('#get-suggestions').animate(
            {opacity: 'show'},
            {duration: 600,
             complete: function(){
                $('.similarities-helper').animate(
                    {opacity: 'show'},
                    {duration: 600,
                     complete: function(){
                        setTimeout(function(){
                            $('.similarities-helper').animate({opacity: 'hide'}, 600);
                        }, 5000);
                     }
                    }
                );
             }
            }
        );
    }, 2000);

    $('body').on('click', '#get-suggestions', function(e){
      e.preventDefault();
      title = $('#title').val();
      suggestions_dialog();
    });
    $('body').on('focusout', '#title', function(){
      if ($('#title').val() != title){
          suggestions_dialog();
      }
    });
});
