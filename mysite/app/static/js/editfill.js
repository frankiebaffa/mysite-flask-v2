$(document).ready(function fillOnReady() {
  $fields = $('.edit-field');
  $($fields).each(function eachField(index, element) {
    $($fields[index]).val($projects[0][index+1]);
  });
  $options = $('option');
  $('select').change(function selectOnChange() {
    index = $('select').val() - 1;
    $($fields).each(function eachFieldFill(j, field) {
      $(field).val($projects[index][j+1]);
    });
  });
});
