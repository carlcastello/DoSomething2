$(document).ready(function() {
    var url = window.location;
    var element = $('.navbar .navbar-nav a').filter(function() {
    return this.href == url || url.href.indexOf(this.href) == 0; }).addClass('active');
    if (element.is('a')) {
        element.addClass('active').addClass('active')
    }
});