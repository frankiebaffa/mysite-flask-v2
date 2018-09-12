$(document).ready(function managePagination() {
  var projectForms = $('.project-form');
  var blogForms = $('.blog-form');
  var articleForms = $('.article-form');
  var projectButtons = $('.project-button');
  var blogButtons = $('.blog-button');
  var articleButtons = $('.article-button');
  var forms = [projectForms, blogForms, articleForms];
  var buttons = [projectButtons, blogButtons, articleButtons];
  $(forms).each(function eachForm(index, element) {
    $(element[0]).show();
    $(buttons[index][0]).removeClass('bg-darker fg-lighter');
    $(buttons[index][0]).addClass('bg-lightest fg-darker');
  });
  $(buttons).each(function eachButtonCategory(i, elements) {
    $(elements).each(function eachButton(j, element) {
      $(element).click(function buttonOnClick() {
        $(buttons[i]).removeClass('bg-lightest fg-darker');
        $(buttons[i]).addClass('bg-darker fg-lighter');
        $(element).removeClass('bg-darker fg-lighter');
        $(element).addClass('bg-lightest fg-darker');
        $(forms[i]).hide();
        $(forms[i][j]).show();
      });
    });
  });
});
