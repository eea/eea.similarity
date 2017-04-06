!function($) {
  $.suggestionsDialog = function(options) {

    var settings = {
      title : 'Please check these possible duplicates:',
      message : 'We have found a list of possible duplicates based on your title choice',
      counter: 0,
      dialog_width: 370
    }

    $.extend(settings, options);

    var SuggestionsDialog = {
      setupDialog: function() {
        var self = this;
        //self.destroyDialog();

        var list = $('<ul/>');
        $.each(settings.suggestions, function(url, sugg){
            list.append($('<li/>')
                .append($('<a/>')
                .attr('title', 'Similarity score: ' + sugg[1])
                .attr('href', url).append(sugg[0]))
            );
        });
        var html = $('<div/>').attr('id', 'similarity-dialog')
                        .append($('<p/>').attr('id', 'similarity-message')
                            .append(settings.message)
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
          title: settings.title,
          show: {
                  effect: "fade",
                  duration: 1000
                },
          position: { my: "right top", at: "right bottom", of: window },
        });

      },

      destroyDialog: function() {
        if ($("#similarity-dialog").length) {
          $(this).dialog("close");
          $('#similarity-dialog').remove();
        }
      },

    };

    SuggestionsDialog.setupDialog();
  };
}(window.jQuery);

$().ready(function(){
        var title = '';
        var url = window.location.href;
        var portal_type = url.split('/')[url.split('/').indexOf('portal_factory')+1];
        $('#title').focusout(function(){
            if ($('#title').val() != title){
                title = $('#title').val();
                $('.similarity-dialog:visible').remove();
                suggestions = $.get('/www/SITE/get_suggestions',
                                    {'portal_type': portal_type, 'title': title},
                                    function(data){
                                        if (Object.keys(data).length){
                                            $.each(data, function(key, value){
                                            });
                                            $.suggestionsDialog({
                                                'suggestions': data
                                            });
                                        }
                                    },
                                    'json')
            }
    });
});
