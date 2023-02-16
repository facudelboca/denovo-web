(function() {
  var elements;
  var windowHeight;

  function init() {
    elements = document.querySelectorAll('.hidden');
    windowHeight = window.innerHeight;
  }

  function checkPosition() {
    for (var i = 0; i < elements.length; i++) {
      var element = elements[i];
      var positionFromTop = elements[i].getBoundingClientRect().top;

      if (positionFromTop - windowHeight <= 0) {
        console.log(' animation started');
        if(element.classList.contains('first-phrase')){
          element.classList.add('first-phrase-animation');
        } else {
          element.classList.add('second-phrase-animation');
        }
        element.classList.remove('hidden');
        console.log('css modified');
      }
    }
  }

  window.addEventListener('scroll', checkPosition);
  window.addEventListener('resize', init);
  window.addEventListener('load', init);

  init();
  checkPosition();

  document.addEventListener('DOMContentLoaded', function(){
    let formulario = document.getElementById('my-form');
    formulario.addEventListener('submit', function() {
      formulario.reset();
    });
  });


})();



