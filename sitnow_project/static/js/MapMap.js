"use strict";
let infowindow;

function addMarkers(map) {
  $.get("/places", function(places) {
    places.forEach(place => {
      var pos = { lat: place.latitude, lng: place.longitude };

      var marker = new google.maps.Marker({
        map,
        title: place.name,
        position: pos
      });
      marker.addListener("click", async () => {
        if (infowindow) {
          infowindow.close();
        }
        var contentString =
          "<div>" +
          place.name +
          "</div>" +
          "<div>" +
          "@ " +
          place.building +
          "</div>";
        infowindow = new google.maps.InfoWindow({
          content: contentString
        });
        infowindow.open(map, marker);
        addPlaceCard(place);
        addCommentCards(place);
        addCommentForm();
      });
    });
  });
}

async function getCardTemplate(filename) {
  let html = await $.get("/static/card_template/" + filename, function(data) {
    return data;
  });
  return html;
}

async function addPlaceCard(place) {
  const card = await getCardTemplate("place_card.html");
  let template = $.parseHTML(card);
  $(template)
    .find("#place_name")
    .text(place.name);
  window.place_name = place.name;
  $(template)
    .find("#place_building")
    .text(place.building);
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
  $(template)
    .find("#hasTable")
    .text(place.permission === null ? "Not required." : place.permission);

  $("#place")
    .empty()
    .append(template);
}

async function addCommentCards(place) {
  $("#comments").empty();
  const comments = await getComment(place);
  const card = await getCardTemplate("comments_card.html");
  comments.forEach(comment => {
    let template = $.parseHTML(card);
    if (document.domain === "sitnow.pythonanywhere.com") {
      $(template)
        .find("#user_image")
        .attr("src", "sitnow.pythonanywhere.com/" + comment.user.picture);
    } else {
      $(template)
        .find("#user_image")
        .attr(
          "src",
          location.protocol +
            "//" +
            document.domain +
            (location.port ? ":" + location.port : "") +
            "/" +
            comment.user.picture
        );
    }

    $(template)
      .find("#rate")
      .text(comment.rate);
    $(template)
      .find("#comment")
      .text(comment.comment);
    $("#comments").append(template);
  });
}

// Initialize and add the map
async function initMap() {
  // The location of Glasgow University
  var uOfG = { lat: 55.872928, lng: -4.289289 };
  // The map, centered at Glasgow University
  var map = new google.maps.Map(document.getElementById("map"), {
    zoom: 16,
    center: uOfG
  });

  addMarkers(map);
}

async function getComment({ name, building, google_id }) {
  return await $.ajax({
    type: "POST",
    url: "/comments/",
    data: {
      name,
      building,
      google_id
    },
    success: async data => {
      return data;
    },
    dataType: "json"
  });
}

async function addCommentForm() {
  $("#new_comment").empty();
  $("#comments").empty();
  const card = await getCardTemplate("comment_card.html");
  let template = $.parseHTML(card);

  let userProfile = await getUser(window.CSRF_TOKEN);
  if (document.domain === "sitnow.pythonanywhere.com") {
    $(template)
      .find("#user_image")
      .attr("src", "sitnow.pythonanywhere.com/" + userProfile.picture);
  } else {
    $(template)
      .find("#user_image")
      .attr(
        "src",
        location.protocol +
          "//" +
          document.domain +
          (location.port ? ":" + location.port : "") +
          "/" +
          userProfile.picture
      );
  }
  $("#new_comment").append(template);
  submitAction(window.CSRF_TOKEN);
}

async function submitAction(csrfmiddlewaretoken) {
  $("#comment_form").submit(async function(event) {
    event.preventDefault();
    await $.ajax({
      type: "POST",
      url: "/comment/",
      data: {
        csrfmiddlewaretoken,
        rate: $("select#rate")
          .children("option:selected")
          .val(),
        comment: $("#current-user-comment").val(),
        place_id: $("#place_id").val()
      },
      success: place => {
        addCommentCards(place);
        $("#comment_form")[0].reset();
        return place;
      },
      dataType: "json"
    });
  });
}

async function getUser(csrfmiddlewaretoken) {
  return await $.ajax({
    type: "POST",
    url: "/getuser/",
    data: {
      csrfmiddlewaretoken
    },
    success: async data => {
      return data;
    },
    dataType: "json"
  });
}
