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
  calculate_stars(template, place.rate);
  $(template)
    .find("#n_rates")
    .text(" (" + place.n_rates + ") ");
  $("#place")
    .empty()
    .append(template);
}

function calculate_stars(template, rate) {
  const starPercentage = (rate / 6) * 100;
  const starPercentageRounded = `${Math.round(starPercentage / 10) * 10}%`;
  $(template)
    .find(".stars-inner")
    .css("width", starPercentageRounded);
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
    let ratting = comment.rate;
    let starString = "";
    // TODO
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
  const starIcons = [
    "#comment-star-1",
    "#comment-star-2",
    "#comment-star-3",
    "#comment-star-4",
    "#comment-star-5"
  ];
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
        console.log(rating);
        for (let i = 0; i < rating; i++) {
          $(starIcons[i])
            .addClass("comment-rate fa-star")
            .removeClass("fa-star-o");
          console.log(starIcons[i]);
        }
        $("#rate").val(rating);
        console.log($(starIcon));
        console.log($("#rate"));
      });
  });

  $(template)
    .find("#submit-comment")
    .click(() => {
      let rateValue = $("#rate").val();
      if (rateValue === "") {
        alert("!!!");
      }
    });

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
