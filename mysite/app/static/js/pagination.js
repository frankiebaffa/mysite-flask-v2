$(document).ready(function pagination() {
  var projects = $('.project-container');
  var blogs = $('.blog-container');
  var articles = $('.article-container');
  var posts = [projects, blogs, articles];
  var projectLinks = $('.project-link');
  var blogLinks = $('.blog-link');
  var articleLinks = $('.article-link');
  var links = [projectLinks, blogLinks, articleLinks];
  $(posts).each(function eachPost(index, element) {
    $(element[0]).show();
    $(links[index][0]).removeClass('bg-darker fg-lighter');
    $(links[index[0]]).addClass('bg-lightest fg-darker');
  });
  $(links).each(function eachLinkGroup(i, elements) {
    $(elements).each(function eachLink(j, element) {
      $(element).click(function postLinkOnClick() {
        $(links[i]).removeClass('bg-lighter fg-darker');
        $(links[i]).addClass('bg-darker fg-lighter');
        $(element).removeClass('bg-darker fg-lighter');
        $(element).addClass('bg-lightest fg-darker');
        $(posts[i]).hide();
        $(posts[i][j]).show();
      });
    });
  });
});

