var phrase = [];
var checkindex = 0;
var errors = 0;
var typing = "";
var accuracy = 100;
$(document).ready(function() {
  $('#errors').text(errors);
  $('#accuracy').text(accuracy+'%');
  $('#typing').on('input propertychange', function() {
    typing = $('#typing').val();
    checkindex = typing.length;
  });
  $('.typespan').each(function eachChar(index, element) {
    phrase.push($(element).text());
  });
  $('#typing').keypress(function( event ) {
    keycheck = event['key'];
    if (keycheck != phrase[checkindex]) {
      errors++;
      $('#errors').text(errors);
      accuracy = ((phrase.length-errors)/phrase.length)*100;
      accuracy = accuracy.toFixed(2);
      $('#accuracy').text(accuracy+'%');
    };
  });
});