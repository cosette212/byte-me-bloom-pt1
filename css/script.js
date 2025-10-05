document.addEventListener('DOMContentLoaded', () => {
    const inputArchivo = document.getElementById('imagen-flor');
    const imgPrevisualizacion = document.getElementById('prev');

    inputArchivo.addEventListener('change', function(e) {
        // Verifica si se ha seleccionado un archivo
        if (e.target.files && e.target.files[0]) {
            const archivo = e.target.files[0];
            const reader = new FileReader();

            // Configura qué hacer cuando el FileReader termina de leer
            reader.onload = function(event) {
                // El resultado es un Data URL que contiene la imagen
                imgPrevisualizacion.src = event.target.result;
                imgPrevisualizacion.style.display = 'block'; // Muestra la imagen
            };

            // Lee el contenido del archivo como un Data URL (base64)
            reader.readAsDataURL(archivo);
        } else {
            // Si no hay archivo, limpia la previsualización
            imgPrevisualizacion.src = '#';
            imgPrevisualizacion.style.display = 'none';
        }
    });
});