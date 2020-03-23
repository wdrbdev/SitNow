"use strict";
let infowindow;
let markers = [];

// Add marker for all places in the database
function addMarkers(map) {
  // Get all places in the database by GET /places/
  $.get("/places", function(places) {
    places.forEach(place => {
      let position = { lat: place.latitude, lng: place.longitude };
      // Pin image url
      let url = "/static/img/pin/green_pin.svg";
      let icon = {
        url,
        scaledSize: new google.maps.Size(30, 30)
      };
      let marker = new google.maps.Marker({
        map,
        icon,
        position,
        title: place.name
      });
      markers.push(marker);

      // onClick event for markers
      marker.addListener("click", async () => {
        // Show info window and close other info window when the marker is clicked
        if (infowindow) {
          infowindow.close();
        }
        let contentString =
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

        // Change the pin image/color
        markers.forEach(marker => {
          marker.setIcon({
            url,
            scaledSize: new google.maps.Size(30, 30)
          });
        });
        marker.setIcon({
          url: "/static/img/pin/yellow_pin.svg",
          scaledSize: new google.maps.Size(30, 30)
        });

        // Show correspond place with comments info as a card
        addPlaceCard(place);
        addCommentCards(place);
        addCommentForm(place);
      });
    });
  });
}

// Get card template html from /static/card_template/
async function getCardTemplate(filename) {
  let html = await $.get("/static/card_template/" + filename, function(data) {
    return data;
  });
  return html;
}

// Add the place information as a card
async function addPlaceCard(place) {
  const card = await getCardTemplate("map_place_card.html");
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
    .html(
      place.hasTable
        ? `<i class="fa fa-check-square" aria-hidden="true"></i>`
        : `<i class="fa fa-minus-square" aria-hidden="true"></i>`
    );
  $(template)
    .find("#hasWifi")
    .html(
      place.hasWifi
        ? `<i class="fa fa-check-square" aria-hidden="true"></i>`
        : `<i class="fa fa-minus-square" aria-hidden="true"></i>`
    );
  $(template)
    .find("#capacity")
    .html(place.capacity);
  $(template)
    .find("#hasMicrowave")
    .html(
      place.hasMicrowave
        ? `<i class="fa fa-check-square" aria-hidden="true"></i>`
        : `<i class="fa fa-minus-square" aria-hidden="true"></i>`
    );
  $(template)
    .find("#hasSocket")
    .html(
      place.hasSocket
        ? `<i class="fa fa-check-square" aria-hidden="true"></i>`
        : `<i class="fa fa-minus-square" aria-hidden="true"></i>`
    );
  $(template)
    .find("#hasFood")
    .html(
      place.hasFood
        ? `<i class="fa fa-check-square" aria-hidden="true"></i>`
        : `<i class="fa fa-minus-square" aria-hidden="true"></i>`
    );
  $(template)
    .find("#hasCoffee")
    .html(
      place.hasCoffee
        ? `<i class="fa fa-check-square" aria-hidden="true"></i>`
        : `<i class="fa fa-minus-square" aria-hidden="true"></i>`
    );
  $(template)
    .find("#noEating")
    .html(
      place.noEating
        ? `<i class="fa fa-check-square" aria-hidden="true"></i>`
        : `<i class="fa fa-minus-square" aria-hidden="true"></i>`
    );
  $(template)
    .find("#hasComputer")
    .html(
      place.hasComputer
        ? `<i class="fa fa-check-square" aria-hidden="true"></i>`
        : `<i class="fa fa-minus-square" aria-hidden="true"></i>`
    );
  $(template)
    .find("#address")
    .text(place.address);
  // $(template)
  //   .find("#permission")
  //   .text(place.permission === null ? "Not required." : place.permission);

  // For favorite
  if (place.favorite !== undefined) {
    if (place.favorite.favorite === true) {
      $(template)
        .find("#place_favorite")
        .html(
          `<i id="place2_favorite" class="fa fa-heart" aria-hidden="true"></i>`
        );
    } else {
      $(template)
        .find("#place_favorite")
        .html(
          `<i id="place2_favorite" class="fa fa-heart-o" aria-hidden="true"></i>`
        );
    }
  }
  $(template)
    .find("#place_favorite")
    .click(e => {
      add_favorite(e, place, window.CSRF_TOKEN);
    });

  // For rating
  calculate_stars(template, place.rate);
  $(template)
    .find("#n_rates")
    .text(" (" + place.n_rates + ") ");
  $("#place")
    .empty()
    .append(template);
}

// Convert 5 stars rating system as percentage from 0% to 100%
function calculate_stars(template, rate) {
  const starPercentage = (rate / 6) * 100;
  const starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;
  $(template)
    .find(".stars-inner")
    .css("width", starPercentageRounded);
}

// Add comments of the place as cards
async function addCommentCards(place) {
  $("#comments").empty();
  const comments = await getComment(place, window.CSRF_TOKEN);
  const card = await getCardTemplate("comments_card.html");

  // For users' profile picture
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

    // For rating
    let ratting = comment.rate;
    let starString = "";
    for (let i = 0; i < ratting; i++) {
      starString += `<i class="fa fa-star" aria-hidden="true" style="color:#f8ce0b;"></i>`;
    }
    $(template)
      .find("#rate")
      .html(starString);
    $(template)
      .find("#comment")
      .text(comment.comment);
    $("#comments").append(template);
  });
}

// Initialize and add the map and markers
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

// POST request to get all comment of the place
async function getComment({ name, building, google_id }, csrfmiddlewaretoken) {
  return await $.ajax({
    type: "POST",
    url: "/comments/",
    data: {
      csrfmiddlewaretoken,
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

// Add comment form to let user to post comment
async function addCommentForm(place) {
  if (window.authenticated !== true) {
    return;
  }
  $("#new_comment").empty();
  $("#comments").empty();
  const card = await getCardTemplate("comment_card.html");
  let template = $.parseHTML(card);

  // For current user's profile picture
  if (window.authenticated === true && window.is_staff !== true) {
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
  }

  // Fill the place id for posting comment to this place
  $(template)
    .find("#place_id")
    .val(place.id);

  // For rating
  const starIcons = [
    "#comment-star-1",
    "#comment-star-2",
    "#comment-star-3",
    "#comment-star-4",
    "#comment-star-5"
  ];
  // Add onClick event for all stars in comment form
  starIcons.forEach(starIcon => {
    $(template)
      .find(starIcon)
      .click(() => {
        starIcons.forEach(starIcon => {
          $(starIcon)
            .removeClass("comment-rate fa-star")
            .addClass("fa-star-o");
        });
        let rating = parseInt(starIcon.charAt(starIcon.length - 1));
        for (let i = 0; i < rating; i++) {
          $(starIcons[i])
            .addClass("comment-rate fa-star")
            .removeClass("fa-star-o");
        }
        $("#rate-input").val(rating);
      });
  });

  $("#new_comment").append(template);
  submitAction(window.CSRF_TOKEN);
}

async function submitAction(csrfmiddlewaretoken) {
  // Add onSubmit event to the comment form
  $("#comment_form").submit(async function(event) {
    event.preventDefault();

    // Check if user fill the rating or not and then post comment
    if ($("#rate-input").val().length === 0) {
      alert("Must choose a rate.");
      return;
    } else {
      await $.ajax({
        type: "POST",
        url: "/comment/",
        data: {
          csrfmiddlewaretoken,
          rate: $("#rate-input").val(),
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

      // Clear the rating after post a comment
      const starIcons = [
        "#comment-star-1",
        "#comment-star-2",
        "#comment-star-3",
        "#comment-star-4",
        "#comment-star-5"
      ];
      starIcons.forEach(starIcon => {
        $(starIcon)
          .removeClass("comment-rate fa-star")
          .addClass("fa-star-o");
      });
    }
  });
}

// Get the current user information
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

// POST request to /favorite/ to add/remove favorite to the place
async function add_favorite(event, { id }, csrfmiddlewaretoken) {
  await $.ajax({
    type: "POST",
    url: "/favorite/",
    data: {
      csrfmiddlewaretoken,
      placeId: id
    },
    success: () => {},
    dataType: "json"
  });

  // Reverse the heart iconfont after clicking
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
