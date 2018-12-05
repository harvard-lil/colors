let page = 0;


function createCasePixel(case_obj) {
  return "<div class='case-pixel'" +
      "data-date='" + case_obj.date + "' " +
      "data-context='" + case_obj.context + "' " +
      "style='background-color: #" + case_obj.hex + "'></div>"
}

function requestNew() {
  let container = $(".container");
  if ($(window).scrollTop() >= ($(window).height() / 2)) {
    $.ajax({
      url: "/date?page=" + page,
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
  // let lastScrollTop = 0;
  // let breakpoint = $(window).height() / 2;
  // let original_breakpoint = breakpoint;
  //
  window.addEventListener("scroll", throttle(requestNew, 500));
  // $(window).scroll();
  // $(window).scroll(function () {
  //
  //   let scrolltop = $(this).scrollTop();
  //   if (scrolltop > lastScrollTop) {
  //     // downscroll code
  //     if (scrolltop >= breakpoint) {
  //       // breakpoint += original_breakpoint;
  //
  //       throttle(requestNew(page), 500);
  //     }
  //   } else {
  //     // upscroll code
  //   }
  //   lastScrollTop = scrolltop;
  //
  // });
  $('.case-pixel').hover(function (e) {
    // console.log($(this).data('date'));

  });
});

