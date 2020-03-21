$(document).ready(function() {
  let site = window.location.pathname.replace(/\//g, "");

  switch (site) {
    case "":
      $("#nav-home").addClass("active");
      break;
    case "aboutus":
    case "forwhom":
    case "tutorial":
      $("#nav-aboutus").addClass("active");
      break;
    case "map":
      $("#nav-map").addClass("active");
      break;
    case "login":
      $("#nav-login").addClass("active");
      break;
    case "favorites":
    case "setting":
      $("#nav-favorites").addClass("active");
      break;
  }
});
