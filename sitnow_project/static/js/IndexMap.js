var map, infoWindow, marker;
var uOfG = { lat: 55.872928, lng: -4.289289 };

// Initialize google map to get user's current location, but not shown on HTML
function initMap() {
  map = new google.maps.Map(document.getElementById("google_map"), {
    zoom: 16,
    center: uOfG
  });

  infoWindow = new google.maps.InfoWindow();


  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function(position) {
        lat = position.coords.latitude;
        lng = position.coords.longitude;
        var pos = { lat, lng };


        // Fill current location
        $("#current_location").attr("data-lat", lat);
        $("#current_location").attr("data-lng", lng);
        fillLocation(pos);


        // Show the option of current location only when Google API can get the current location
        showCurrentLocation();
      },
      function() {
        handleLocationError(true, infoWindow, map.getCenter());
      }
    );
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
  }
}

// Handle error (written by Google https://developers.google.com/maps/documentation/javascript/geolocation)
function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
  hideCurrentLocation();
}

// Hide the option of current location
function hideCurrentLocation() {
  $("#current_location")
    .prop("hidden", true)
    .prop("disabled", true)
    .val("");
}

// Show the option of current location
function showCurrentLocation() {
  $("#current_location")
    .prop("hidden", false)
    .prop("disabled", false)
    .val("current_location");
}

// Fill latitude and longitude of current location into form
function fillLocation({ lat, lng }) {
  $("#id_latitude").val(lat);
  $("#id_longitude").val(lng);
}

$(document).ready(function() {
  // Add click event to the choice/filter button
  const idArray = [
    "hasTable",
    "hasWifi",
    "hasMicrowave",
    "hasSocket",
    "hasFood",
    "noEating",
    "hasCoffee",
    "hasComputer"
  ];
  idArray.forEach(id => {
    $("#" + id).click(function() {
      let data = $("#id_" + id).val();
      if (data === "None") {
        $("#id_" + id).val("True");
        $(this)
          .removeClass("btn-light")
          .addClass("btn-primary");
      } else {
        $("#id_" + id).val("None");
        $(this)
          .removeClass("btn-primary")
          .addClass("btn-light");
      }
    });
  });
  

  // If location info of dropdown choice changes, change the latitude and longitude value in the form
  $("select#location").change(function() {
    if (
      $(this)
        .children("option:selected")
        .val() === "current_location"
    ) {
      initMap();
    }
    let dataset = $(this)
      .children("option:selected")
      .data();
    $("#id_latitude").val(dataset.lat);
    $("#id_longitude").val(dataset.lng);
  });
});
