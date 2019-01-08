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
  let newParams = "?";
  let allParams = [];
  if (window.location.search.length > 0) {
    allParams = window.location.search.split("?")[1].split("&");
    for (idx in allParams) {
      if (allParams[idx].indexOf(key + "=") < 0) {
        newParams += allParams[idx] + "&"
      }
    }
  }
  newParams += key + "=" + val;
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
        let year = $(this).attr('data-date').substring(0, 4);
        $('.case-title').text(title);
        $('.case-text').text(text);
        $('.case-year').text(year);
      });
}

function colorChange() {
  console.log("changing color!")
  let colorInput = $("#color");
  let color = colorInput.val();
  let body = $('body');
  if (color.length > 0) {
    $.post("/create", {"color": color})
        .done(function(data){
          console.log("success!", data);
          body.css('backgroundColor', data.color)
        })
  }
}

$(function () {
  loadMore = document.getElementById("load-more");
  if (loadMore) {
    loadMore.addEventListener('click', function (e) {
      requestNew();
      e.stopPropagation();
    });
  }

  let colorInput = document.getElementById("color");
  if (colorInput) {
    colorInput.addEventListener("keypress", colorChange);
  }
  addCaseContext();
});
