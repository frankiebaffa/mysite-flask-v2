typing = [];
phrase = [];
keycount = 0;
$(document).ready(function() {
  $('.typespan').each(function eachChar(index, element) {
    phrase.push($(element).text());
  });
  $('#typing').keypress(function( event ) {
    keycount++;
  });
  $('#typing').on('input propertychange', function() {
    typing = $('#typing').val();
    if (typing == phrase.join('') && keycount < typing.length) {
      $('#typing-header').text('CHEATER');
      $('#typing').attr('disabled', 'true');
    } else if (typing == phrase.join('')) {
      $('#typing').attr('disabled', 'true');
    };
  });
});