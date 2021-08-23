(function (e) {
  var o,
    i = e(window),
    a = e("head"),
    t = e("body");
  breakpoints({
    xlarge: ["1281px", "1680px"],
    large: ["981px", "1280px"],
    medium: ["737px", "980px"],
    small: ["481px", "736px"],
    xsmall: ["361px", "480px"],
    xxsmall: [null, "360px"],
    "xlarge-to-max": "(min-width: 1681px)",
    "small-to-xlarge": "(min-width: 481px) and (max-width: 1680px)",
  }),
    i.on("load", function () {
      window.setTimeout(function () {
        t.removeClass("is-preload");
      }, 100);
    }),
    i.on("resize", function () {
      t.addClass("is-resizing"),
        clearTimeout(o),
        (o = setTimeout(function () {
          t.removeClass("is-resizing");
        }, 100));
    }),
    (browser.canUse("object-fit") && "safari" != browser.name) ||
      e(".image.object").each(function () {
        var o = e(this),
          i = o.children("img");
        i.css("opacity", "0"),
          o
            .css("background-image", 'url("' + i.attr("src") + '")')
            .css(
              "background-size",
              i.css("object-fit") ? i.css("object-fit") : "cover"
            )
            .css(
              "background-position",
              i.css("object-position") ? i.css("object-position") : "center"
            );
      });
  var s = e("#sidebar"),
    n = s.children(".inner");
  breakpoints.on("<=large", function () {
    s.addClass("inactive");
  }),
    breakpoints.on(">large", function () {
      s.removeClass("inactive");
    }),
    "android" == browser.os &&
      "chrome" == browser.name &&
      e(
        "<style>#sidebar .inner::-webkit-scrollbar { display: none; }</style>"
      ).appendTo(a),
    e('<a href="#sidebar" class="customToggle">Toggle</a>')
      .appendTo(s)
      .on("click", function (e) {
        e.preventDefault(), e.stopPropagation(), s.toggleClass("inactive");
      }),
    s.on("click", "a", function (o) {
      if (!breakpoints.active(">large")) {
        var i = e(this),
          a = i.attr("href"),
          t = i.attr("target");
        o.preventDefault(),
          o.stopPropagation(),
          a &&
            "#" != a &&
            "" != a &&
            (s.addClass("inactive"),
            setTimeout(function () {
              "_blank" == t ? window.open(a) : (window.location.href = a);
            }, 500));
      }
    }),
    s.on("click touchend touchstart touchmove", function (e) {
      breakpoints.active(">large") || e.stopPropagation();
    }),
    t.on("click touchend", function (e) {
      breakpoints.active(">large") || s.addClass("inactive");
    }),
    i.on("load.sidebar-lock", function () {
      var e, o;
      1 == i.scrollTop() && i.scrollTop(0),
        i
          .on("scroll.sidebar-lock", function () {
            var a, t;
            breakpoints.active("<=large")
              ? n.data("locked", 0).css("position", "").css("top", "")
              : ((a = Math.max(e - o, 0)),
                (t = Math.max(0, i.scrollTop() - a)),
                1 == n.data("locked")
                  ? t <= 0
                    ? n.data("locked", 0).css("position", "").css("top", "")
                    : n.css("top", "")
                  : t > 0 &&
                    n
                      .data("locked", 1)
                      .css("position", "").css("top", ""));
          })
          .on("resize.sidebar-lock", function () {
            (o = i.height()),
              (e = n.outerHeight() + 30),
              i.trigger("scroll.sidebar-lock");
          })
          .trigger("resize.sidebar-lock");
    });
  var r = e("#menu"),
    c = r.children("ul").find(".opener");
  c.each(function () {
    var o = e(this);
    o.on("click", function (e) {
      e.preventDefault(),
        c.not(o).removeClass("active"),
        o.toggleClass("active"),
        i.triggerHandler("resize.sidebar-lock");
    });
  });
})(jQuery);