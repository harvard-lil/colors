let page = 0;
let requestPath = window.location.pathname;

function createCasePixel(case_obj) {
  return "<div class='case-pixel'" +
      "data-date='" + case_obj.date + "' " +
      "data-context='" + case_obj.context + "' " +
      "style='background-color: #" + case_obj.hex +
      "'>" +
      "<span class='tooltiptext'><h2>"  +
      case_obj.captured_text + "</h2>" +
      "<em>" + case_obj.context + "</em>" +
      "<br/>" +
      case_obj.date +
      "<br/>" + case_obj.name_abbreviation + "</span></div>"
}

function requestNew() {
  let container = $(".container");
  if ($(window).scrollTop() >= ($(window).height() / 2)) {
    $.ajax({
      url: requestPath + "?page=" + page,
      success: function (data) {
        if (data.length === 0) {
          // done with loading data, return empty;
          return
        }

        for (let i = 0; i < data.length - 1; i++) {
          let newCasePixel = createCasePixel(data[i]);
          container.append(newCasePixel);
        }
        console.log("appending data", $('.case-pixel').length, data.length, "page number", page);

        page += 1;
        return data;
      },
      error: function (err) {
        console.log("error!");
        return err;
      }
    })
  }
}

function throttle(callback, limit) {
  let wait = false;
  return function () {
    if (!wait) {
      callback.call();
      wait = true;
      setTimeout(function () {
        wait = false;
      }, limit);
    }
  }
}


$(function () {
  window.addEventListener("scroll", throttle(requestNew, 500));
  $('.case-pixel').hover(function (e) {
  });
});

