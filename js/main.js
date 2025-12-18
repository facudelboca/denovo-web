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

  setTimeout(function() {
    document.getElementById('my-form').reset();
  }, 1500);


})();

// Función para inicializar componentes
function initComponents() {
  // Carrusel de imágenes (si existe en la página)
  const images = document.querySelectorAll(".carousel img");
  if (images.length > 0) {
    let index = 1; // Imagen activa inicial

    function updateCarousel() {
      images.forEach((img, i) => {
        img.classList.remove("active", "prev", "next");

        if (i === index) {
          img.classList.add("active");
        } else if (i === (index - 1 + images.length) % images.length) {
          img.classList.add("prev");
        } else if (i === (index + 1) % images.length) {
          img.classList.add("next");
        }
      });
    }

    function nextImage() {
      index = (index + 1) % images.length;
      updateCarousel();
    }

    setInterval(nextImage, 3000); // Cambia la imagen cada 3 segundos
    updateCarousel();
  }

  // Inclusión de fragmentos HTML comunes (navbar, footer, iconos sociales)
  const includeTargets = document.querySelectorAll("[data-include]");
  includeTargets.forEach((el) => {
    const url = el.getAttribute("data-include");
    if (!url) return;

    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error("No se pudo cargar el fragmento: " + url);
        }
        return response.text();
      })
      .then((html) => {
        el.innerHTML = html;
      })
      .catch((error) => {
        console.error("Error cargando componente:", url, error);
      });
  });
}

// Ejecutar cuando el DOM esté listo (funciona tanto si el script está en head como en body)
if (document.readyState === 'loading') {
  document.addEventListener("DOMContentLoaded", initComponents);
} else {
  // El DOM ya está listo, ejecutar inmediatamente
  initComponents();
}


