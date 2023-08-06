if (document.getElementsByClassName("vTextField")){




var imported = document.createElement('script');
var imported2 = document.createElement('script');
imported.src = 'https://host.pathomation.com/sdk/pma.ui.documentation/pma.ui.js';
document.head.appendChild(imported);
imported2.src = 'https://code.jquery.com/jquery-3.1.0.js';
document.head.appendChild(imported2);

$(document).ready(function() {
  $('<button id="connection"  onclick="testConnection()" style="margin-bottom:5px;position:relative; left:0%; font-weight: bold;" type="button">Test connection</button>').prependTo('.submit-row');
  document.getElementById("id_PMACorePassword").type = "password";
});





function testConnection() {
        var button = document.getElementById('connection');
        button.remove();
        $('<button id="connection"  onclick="testConnection()" style="margin-bottom:5px; font-weight: bold;" type="button">Test connection</button>').prependTo('.submit-row');

        console.log("PMA.UI loaded: " + PMA.UI.getVersion());


        // create a context
        var context = new PMA.UI.Components.Context({ caller: "Django cms plugin" });
        var username = document.getElementById("id_PMACoreUsername").value;
        var password = document.getElementById("id_PMACorePassword").value;

        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "https://myapi.pathomation.com/oauth/token",
            "method": "POST",
            "data": {
                "grant_type": "password",
                "client_id": "6",
                "client_secret": "9APfPpHZMoDKe6ECVYweIrAaopFXVqOSlsrfNGam",
                "username": username,
                "password": password,
                "scope": "*"
            },
            "headers": {
                "accept": "application/json"
            }
        }



        $.ajax(settings).done(function (response) {

                    $('<p style="color: green!important;"> Connection Succesful!</p>').appendTo('#connection');

                }).fail(function (jqXHR, textStatus, error) {

                    $('<p style="color: red!important;"> Connection failed.</p>').appendTo('#connection');
                  });


        };
}
