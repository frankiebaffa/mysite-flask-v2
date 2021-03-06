$(document).ready(function fillOnReady() {
  var tdown = new TurndownService();
  // assign all project-edit fields to variable
  var $projectFields = $('.project-edit');
  // assign all blog-edit fields to variable
  var $blogFields = $('.blog-edit');
  // assign all review-edit fields to variable
  var $reviewFields = $('.review-edit');
  var $musicFields = $('.music-edit');
  // add other content types here
  
  // assign all field categories to variable
  //   append with additional content categories if neccessary
  var $fields = [];
  if ($projectFields.length !== 0) {
    $fields.push($projectFields)
  };
  if ($blogFields.length !== 0) {
    $fields.push($blogFields)
  };
  if ($reviewFields.length !== 0) {
    $fields.push($reviewFields)
  };
  if ($musicFields.length !== 0) {
    $fields.push($musicFields)
  };

  // for each field category in $fields
  $($fields).each(function eachFieldCategory(i, category) {
    // for each field in each field category
    $(category).each(function eachField(j, field) {
      // populate field with the first post in the corresponding category
      var content = $content[i][0][j]
      if ($(field).is('textarea')) {
        content = tdown.turndown(content);
        content = tdown.turndown(content);
      };
      $(field).val(content);
    });
  });

  // assign all select fields to variable $selects
  var $selects = $('select');
  // for each select field in $selects
  $($selects).each(function eachCategorySelect(i, categorySelect) {
    // on change of select field value
    $(categorySelect).change(function selectOnChange() {
      // set index as the value of selectfield - 1
      index = $(this).val() - 1;
      // for each field in same category of select field changed
      $($fields[i]).each(function eachFieldInCategory(j, field) {
        // populate the field with the content within
        // the corresponding category beginning at index of
        // this each index + 1
        var content = $content[i][index][j];
        if ($(field).is('textarea')) {
          content = tdown.turndown(content);
          content = tdown.turndown(content);
        };
        $(field).val(content);
      });
    });
  });
});
