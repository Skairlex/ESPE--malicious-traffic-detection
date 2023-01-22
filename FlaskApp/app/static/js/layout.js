

        $(function() {
          $('a#test').on('click', function(e) {
            e.preventDefault()
            $.getJSON('/background_process_test',
                function(data) {
              //do nothing
            });
            return false;
          });
        });