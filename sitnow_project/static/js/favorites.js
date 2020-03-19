async function addFavorite(event, placeId, csrfmiddlewaretoken) {
  await $.ajax({
    type: "POST",
    url: "/favorite/",
    data: {
      csrfmiddlewaretoken,
      placeId
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
