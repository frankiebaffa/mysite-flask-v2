$(".hover-invert-all").hover(function invertHoverIn() {
  if ($(this).hasClass("bg-darkest")) {
    $(this).hover(function() {
      $(this).removeClass("bg-darkest").addClass("bg-lightest");
    },
    function() {
      $(this).addClass("bg-darkest").removeClass("bg-lightest");
    });
  };
  if ($(this).hasClass("bg-darker")) {
    $(this).hover(function() {
      $(this).removeClass("bg-darker").addClass("bg-lighter");
    },
    function() {
      $(this).addClass("bg-darker").removeClass("bg-lighter");
    });
  };
  if ($(this).hasClass("bg-dark")) {
    $(this).hover(function() {
      $(this).removeClass("bg-dark").addClass("bg-light");
    },
    function() {
      $(this).addClass("bg-dark").removeClass("bg-light");
    });
  };
  if ($(this).hasClass("bg-light")) {
    $(this).hover(function() {
      $(this).removeClass("bg-light").addClass("bg-dark");
    },
    function() {
      $(this).addClass("bg-light").removeClass("bg-dark");
    });
  };
  if ($(this).hasClass("bg-lighter")) {
    $(this).hover(function() {
      $(this).removeClass("bg-lighter").addClass("bg-darker");
    },
    function() {
      $(this).addClass("bg-lighter").removeClass("bg-darker");
    });
  };
  if ($(this).hasClass("bg-lightest")) {
    $(this).hover(function() {
      $(this).removeClass("bg-lightest").addClass("bg-darkest");
    },
    function() {
      $(this).addClass("bg-lightest").removeClass("bg-darkest");
    });
  };
  if ($(this).hasClass("fg-darkest")) {
    $(this).hover(function() {
      $(this).removeClass("fg-darkest").addClass("fg-lightest");
    },
    function() {
      $(this).addClass("fg-darkest").removeClass("fg-lightest");
    });
  };
  if ($(this).hasClass("fg-darker")) {
    $(this).hover(function() {
      $(this).removeClass("fg-darker").addClass("fg-lighter");
    },
    function() {
      $(this).addClass("fg-darker").removeClass("fg-lighter");
    });
  };
  if ($(this).hasClass("fg-dark")) {
    $(this).hover(function() {
      $(this).removeClass("fg-dark").addClass("fg-light");
    },
    function() {
      $(this).addClass("fg-dark").removeClass("fg-light");
    });
  };
  if ($(this).hasClass("fg-light")) {
    $(this).hover(function() {
      $(this).removeClass("fg-light").addClass("fg-dark");
    },
    function() {
      $(this).addClass("fg-light").removeClass("fg-dark");
    });
  };
  if ($(this).hasClass("fg-lighter")) {
    $(this).hover(function() {
      $(this).removeClass("fg-lighter").addClass("fg-darker");
    },
    function() {
      $(this).addClass("fg-lighter").removeClass("fg-darker");
    });
  };
  if ($(this).hasClass("fg-lightest")) {
    $(this).hover(function() {
      $(this).removeClass("fg-lightest").addClass("fg-darkest");
    },
    function() {
      $(this).addClass("fg-lightest").removeClass("fg-darkest");
    });
  };
})
