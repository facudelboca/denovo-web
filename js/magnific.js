
jQuery(document).ready(function () {
    $('.magnific').magnificPopup({
    type:'image',
    removalDelay: 300,
    mainClass: 'mfp-fade'
  });
    
  $('.magnific-youtube, .magnific-vimeo').magnificPopup({
    disableOn: 700,
    type: 'iframe',
    mainClass: 'mfp-fade',
    removalDelay: 300,
    preloader: false,
    fixedContentPos: false
});
});