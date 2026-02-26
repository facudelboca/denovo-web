// Carga síncrona del head común para reducir duplicación
(function loadHeadPartial() {
  var include = document.querySelector('meta[data-head-include]');
  if (!include) return;

  var url = include.getAttribute('data-head-include');
  if (!url) return;

  try {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, false); // síncrono para garantizar carga temprana
    xhr.send();

    if (xhr.status >= 200 && xhr.status < 300) {
      include.insertAdjacentHTML('beforebegin', xhr.responseText);
    } else {
      console.error('No se pudo cargar el head común:', url, xhr.status);
    }
  } catch (error) {
    console.error('Error cargando el head común:', error);
  }
})();

