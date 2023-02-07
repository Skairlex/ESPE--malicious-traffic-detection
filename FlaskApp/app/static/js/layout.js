

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

        function MO_informacion() {
          var x = document.getElementById("informacion");
          var y = document.getElementById("contactos");
          var z = document.getElementById("analisis");

          x.style.display = "block";

          y.style.display = "none";
          z.style.display = "none";

        }

        function MO_contactos() {
          var x = document.getElementById("informacion");
          var y = document.getElementById("contactos");
          var z = document.getElementById("analisis");

          y.style.display = "block";

          x.style.display = "none";
          z.style.display = "none";
          
        }

        function MO_analisis() {
          var x = document.getElementById("informacion");
          var y = document.getElementById("contactos");
          var z = document.getElementById("analisis");

          z.style.display = "block";

          x.style.display = "none";
          y.style.display = "none";
          
        }