// Add a place to user's favorite by POST to/favorite/
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
