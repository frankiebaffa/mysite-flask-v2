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
  });
  $(links).each(function eachLinkGroup(i, elements) {
    $(elements).each(function eachLink(j, element) {
      $(element).click(function postLinkOnClick() {
        $(posts[i]).hide();
        $(posts[i][j]).show();
      });
    });
  });
});

