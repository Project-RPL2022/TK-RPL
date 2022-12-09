/* Variables */

const roomServiceOrderStatusColor = {
  WAITING: "text-orange-300",
  PROCESSED: "text-green-500",
  REJECTED: "text-red-500",
  FINISHED: "text-black",
};

/* Functions */

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function getPrice(price) {
  return new Intl.NumberFormat("en-DE").format(price);
}

function getDateString(date) {
  var options = { year: 'numeric', month: 'long', day: 'numeric' };
  let data = new Date(date);
  return data.toLocaleDateString("en-US", options);
}