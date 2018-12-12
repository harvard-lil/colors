let page = 0;
let requestPath = window.location.pathname;
let loadMore = "";

function createCasePixel(case_obj) {
  let pixel = document.createElement("div");
  pixel.className = "case-pixel";
  pixel.dataset.date = case_obj.date;
  pixel.dataset.context = case_obj.context;
  pixel.style = "background-color: #" + case_obj.hex;
  return pixel
}
function createNewRequestPath(key, val) {
  // preserve all params
  let allParams = window.location.search.split("?")[1].split("&");
  let newParams = "?";
  console.log("all old params", allParams);
  for (idx in allParams) {
    if (allParams[idx].indexOf(key+"=") < 0) {
      newParams += allParams[idx] + "&"
    }
  }
  newParams += key + "=" + val;
  console.log("new url:", window.location.pathname + newParams)
  return window.location.pathname + newParams;
}

function requestNew() {
  loadMore.disabled = true;
  if ($(window).scrollTop() >= ($(window).height() / 2)) {
    $.ajax({
      url: createNewRequestPath("page", page),
      success: function (data) {
        if (data.length === 0) {
          // done with loading data, return empty;
          return
        }
        let c = document.createDocumentFragment();
        for (let i = 0; i < data.length - 1; i++) {
          let newCasePixel = createCasePixel(data[i]);
          c.appendChild(newCasePixel);
        }
        //TODO: hover event doesn't seem to be included here
        let el = document.getElementById('pixel-container');
        el.appendChild(c);

        page += 1;
        loadMore.disabled = false;
        return data;

      },
      error: function (err) {
        console.log("error!", arguments);
        return err;
      },
      finally: function () {
        addCaseContext();
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

function addCaseContext() {

  $('.case-pixel').off()
      .hover(function (e) {
        let title = $(this).attr('data-title');
        let text = $(this).attr('data-text');
        let year = $(this).attr('data-date').substring(0,4);
        $('.case-title').text(title);
        $('.case-text').text(text);
        $('.case-year').text(year);
      });
}


$(function () {
  loadMore = document.getElementById("load-more");
  loadMore.addEventListener('click', function (e) {
    requestNew();
    e.stopPropagation();
  });

  addCaseContext();
  window.dothis = function () {
    addCaseContext();
  }
});
