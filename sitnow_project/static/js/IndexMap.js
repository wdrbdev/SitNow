// Note: This example requires that you consent to location sharing when
// prompted by your browser. If you see the error "The Geolocation service
// failed.", it means you probably did not give permission for the browser to
// locate you.
var map, infoWindow, marker;
var uOfG = { lat: 55.872928, lng: -4.289289 };

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
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

        $("#current_location").attr("data-lat", lat);
        $("#current_location").attr("data-lng", lng);

        infoWindow.setPosition(pos);
        infoWindow.setContent("Location set.");
        infoWindow.open(map);
        // map.setCenter(pos);

        fillLocation(pos);
      },
      function() {
        handleLocationError(true, infoWindow, map.getCenter());
      }
    );
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, infoWindow, map.getCenter());
    hideCurrentLocation();
  }

  google.maps.event.addListener(map, "click", event => {
    if (document.infowindow) {
      document.infowindow.close();
    }
    content = "Location set.";
    infowindow = new google.maps.InfoWindow({ content });
    infowindow.open(map, marker);
    infoWindow.setPosition(event.latLng);
    infoWindow.open(map);
    // map.setCenter(event.latLng);

    fillLocation(event.latLng);
  });
}

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

function hideCurrentLocation() {
  $("#current_location")
    .prop("hidden", "hidden")
    .val("");
}

function fillLocation({ lat, lng }) {
  $("#id_latitude").val(lat);
  $("#id_longitude").val(lng);
}

function backup() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 55.872928, lng: -4.289289 },
    zoom: 16
  });

  google.maps.event.addListener(map, "click", event => {
    fillLocation(event.latLng);
    setMarker(event.latLng);
  });
}

$(document).ready(function() {
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
