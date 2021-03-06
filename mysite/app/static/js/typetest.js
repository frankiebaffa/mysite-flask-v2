$(document).ready(function onReady() {
  var phrase = [];
  var typing = "";
  var timer = 0;
  var wpm = 0;
  var highcount = 0;
  $('.typespan').each(function eachChar(index, element) {
    phrase.push($(element).text());
  });
  $('#typing').on('input propertychange', function typingChange() {
    typing = $('#typing').val();
    for (i = 0; i < typing.length; i++) {
      if (typing[i] == phrase[i]) {
        var countstring = (i+1).toString();
        $("#typing-"+countstring).css("color", "green");
        $("#typing-"+countstring).css("background-color", "inherit");
      } else if (typing[i] != phrase[i]){
        var countstring = (i+1).toString();
        $("#typing-"+countstring).css("color", "red");
        if (phrase[i] == " ") {
          $('#typing-'+countstring).css("background-color", "red");
        };
      };
    };
    if (typing.length < phrase.length) {
      for (i = typing.length; i < phrase.length; i++) {
        var countstring = (i+1).toString();
        $("#typing-"+countstring).css("color", "var(--lighter)");
        $("#typing-"+countstring).css("background-color", "inherit")
      };
    };
  });
  $('#timer').text(timer);
  $('#wpm').text(wpm);
  $('#typing').one('input propertychange', function timerInit() {
    setInterval(function timerStart() {
      timer++;
      if (typing != phrase.join('')) {
        $('#timer').text(timer);
      };
    }, 1000);
    setInterval(function wpmCalc() {
      if (typing !=phrase.join('')) {
        if (typing.length > highcount) { highcount = typing.length; };
        if (timer == 0) { wpm = 0; }
        else { wpm = ((highcount/5)/(timer/60).toString()) };
        $('#wpm').text(Math.round(wpm));
       };
    }, 1000);
  });
});
