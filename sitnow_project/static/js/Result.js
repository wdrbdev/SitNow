let infowindow, marker;

async function getPlace({ name, building }, csrfmiddlewaretoken) {
  let place = await $.ajax({
    type: "POST",
    url: "/place/",
    data: {
      csrfmiddlewaretoken,
      name,
      building
    },
    success: async data => {
      return data;
    },
    dataType: "json"
  });
  return place;
}

async function getCardTemplate(filename) {
  let html = await $.get("/static/card_template/" + filename, function(data) {
    return data;
  });
  return html;
}

async function addPlaceCard(place, target_id) {
  const card = await getCardTemplate("result_place_card.html");
  let template = $.parseHTML(card);
  $(template)
    .find("#place_name")
    .text(place.name);
  window.place_name = place.name;
  $(template)
    .find("#place_building")
    .text("@ " + place.building);
  window.place_building = place.building;
  $(template)
    .find("#google_id")
    .text(place.google_id);
  window.google_id = place.google_id;
  $(template)
    .find("#place_img")
    .attr("src", place.image_url);
  $(template)
    .find("#hasTable")
    .text(place.hasTable ? "Yes" : "No");
  $(template)
    .find("#hasWifi")
    .text(place.hasWifi ? "Yes" : "No");
  $(template)
    .find("#capacity")
    .text(place.capacity);
  $(template)
    .find("#hasMicrowave")
    .text(place.hasMicrowave ? "Yes" : "No");
  $(template)
    .find("#hasSocket")
    .text(place.hasSocket ? "Yes" : "No");
  $(template)
    .find("#hasFood")
    .text(place.hasFood ? "Yes" : "No");
  $(template)
    .find("#hasCoffee")
    .text(place.hasCoffee ? "Yes" : "No");
  $(template)
    .find("#noEating")
    .text(place.noEating ? "Yes" : "No");
  $(template)
    .find("#hasComputer")
    .text(place.hasComputer ? "Yes" : "No");
  // $(template)
  //   .find("#permission")
  //   .text(place.permission === null ? "Not required." : place.permission);
  let starPercentage = (place.rate / 5) * 100;
  let starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;
  $(template)
    .find(".stars-inner")
    .css("width", starPercentageRounded);
  // Add mini map
  initDirectionMap(template, target_id);

  target_ids = ["#place1", "#place2", "#place3"];
  target_ids.forEach(id => {
    if ($(id).length !== 0) {
      $(id + "_card").empty();
      if (id === target_id) {
        $(id + "_card").append(template);
      }
    }
  });
}

// Initialize and add the map
async function initMap() {
  // The location of Glasgow University
  if ($("#place1").length !== 0) {
    var startLocation = {
      lat: parseFloat($("#place1").data().latitude),
      lng: parseFloat($("#place1").data().longitude)
    };
  } else {
    var startLocation = {
      lat: parseFloat($("#start").data().latitude),
      lng: parseFloat($("#start").data().longitude)
    };
  }
  // The map, centered at Glasgow University
  var map = new google.maps.Map(document.getElementById("map"), {
    zoom: 16,
    center: startLocation
  });

  // Try HTML5 geolocation.
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function(position) {
        lat = position.coords.latitude;
        lng = position.coords.longitude;
        var pos = { lat, lng };
        $("#current_location").attr("data-lat", lat);
        $("#current_location").attr("data-lng", lng);

        fillLocation(pos);
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

  place_targets = ["#place1", "#place2", "#place3"];
  place_targets.forEach(place_target => {
    if ($(place_target).length !== 0) {
      var marker = new google.maps.Marker({
        map,
        title: $(place_target).data().name,
        position: {
          lat: parseFloat($(place_target).data().latitude),
          lng: parseFloat($(place_target).data().longitude)
        }
      });

      marker.addListener("click", () => {
        if (infowindow) {
          infowindow.close();
        }
        var contentString =
          "<div>" +
          $(place_target).data().name +
          "</div>" +
          "<div>" +
          "@ " +
          $(place_target).data().building +
          "</div>";
        infowindow = new google.maps.InfoWindow({
          content: contentString
        });
        infowindow.open(map, marker);
      });
    }
  });
}

async function initMapPlace1() {
  if ($("#place1").length !== 0) {
    place = await getPlace($("#place1").data(), window.CSRF_TOKEN);
    addPlaceCard(place, "#place1");
  }
}
async function initMapPlace2() {
  if ($("#place2").length !== 0) {
    place = await getPlace($("#place2").data(), window.CSRF_TOKEN);
    addPlaceCard(place, "#place2");
  }
}
async function initMapPlace3() {
  if ($("#place3").length !== 0) {
    place = await getPlace($("#place3").data(), window.CSRF_TOKEN);
    addPlaceCard(place, "#place3");
  }
}

function fillLocation({ lat, lng }) {
  $("#id_latitude").val(lat);
  $("#id_longitude").val(lng);
}

function initDirectionMap(template, target_id) {
  $("#google_map").prop("hidden", "hidden");

  var directionsService = new google.maps.DirectionsService();
  var directionsRenderer = new google.maps.DirectionsRenderer();

  var startLocation = {
    lat: parseFloat($("#start").data().latitude),
    lng: parseFloat($("#start").data().longitude)
  };

  // The map, centered at Glasgow University
  var map = new google.maps.Map(
    $(template)
      .find("#mini_map")
      .get(0),
    {
      zoom: 16,
      center: startLocation
    }
  );
  directionsRenderer.setMap(map);
  calculateAndDisplayRoute(target_id, directionsService, directionsRenderer);
}

function calculateAndDisplayRoute(
  target_id,
  directionsService,
  directionsRenderer
) {
  directionsService.route(
    {
      origin: {
        lat: parseFloat($("#start").data().latitude),
        lng: parseFloat($("#start").data().longitude)
      },
      destination: {
        lat: parseFloat($(target_id).data().latitude),
        lng: parseFloat($(target_id).data().longitude)
      },
      travelMode: "WALKING"
    },
    function(response, status) {
      if (status === "OK") {
        directionsRenderer.setDirections(response);
      } else {
        window.alert("Directions request failed due to " + status);
      }
    }
  );
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
    .prop("hidden", true)
    .prop("disabled", true)
    .val("");
}

function showCurrentLocation() {
  $("#current_location")
    .prop("hidden", false)
    .prop("disabled", false)
    .val("current_location");
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

  const place_ids = ["#place1", "#place2", "#place3"];
  place_ids.forEach(place_id => {
    if ($(place_id).length !== 0) {
      $(place_id + "_favorite").click(e => {
        add_favorite(e, $(place_id).data(), window.CSRF_TOKEN);
      });
    }
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

  insert_stars();
});

function insert_stars() {
  target_ids = ["#place1", "#place2", "#place3"];
  target_ids.forEach(id => {
    if ($(id).length !== 0) {
      let data = $(id).data();
      let starPercentage = (data.rate / 5) * 100;
      let starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;
      $(id)
        .find(".stars-inner")
        .css("width", starPercentageRounded);
    }
  });
}

async function add_favorite(event, { placeId }, csrfmiddlewaretoken) {
  await $.ajax({
    type: "POST",
    url: "/favorite/",
    data: {
      csrfmiddlewaretoken,
      placeId
    },
    success: data => {
      console.log(data);
    },
    dataType: "json"
  });
  if (event.target.classList.contains("fa-heart")) {
    $(event.target)
      .removeClass("fa-heart")
      .addClass("fa-heart-o");
  } else {
    $(event.target)
      .removeClass("fa-heart-o")
      .addClass("fa-heart");
  }
}
