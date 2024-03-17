function obtenerCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function convertirTablaAJSON(selector) {
    const todasLasTablas = document.querySelectorAll(selector);
    const dataDeTodasLasTablas = Array.from(todasLasTablas).map(tabla => {
        // Buscar el elemento h4 relacionado con cada tabla
        let tituloElemento = tabla.closest('.table-responsive').previousElementSibling;
        
        // Verificar si el elemento encontrado es un h4 o utilizar 'Sin título'
        const titulo = tituloElemento && tituloElemento.tagName === 'H4' ? tituloElemento.innerText : 'Sin título';
        
        const filas = Array.from(tabla.rows).map(tr => {
            return Array.from(tr.cells).map(td => td.textContent.trim());
        });
        return { titulo, filas }; // Devuelve un objeto con el título y las filas de cada tabla
    });
    return dataDeTodasLasTablas;
}

function convertirGraficasAImagenesBase64() {
    // Buscar todos los elementos canvas en el documento
    const graficos = document.querySelectorAll('canvas');
    const graficosIds = Array.from(graficos).map(grafico => grafico.id);

    // Proceder como antes, pero usando los IDs obtenidos dinámicamente
    return Promise.all(
        graficosIds.map(id => 
            new Promise(resolve => {
                const canvas = document.getElementById(id);
                if (canvas) {
                    resolve(canvas.toDataURL());
                } else {
                    resolve(null);
                }
            })
        )
    );
}

function exportarReporte() {
    const titulo = document.querySelector('h3').innerText;
    const descripcion = document.querySelector('p').innerText;
    const tablasDatos = convertirTablaAJSON('.table');

    convertirGraficasAImagenesBase64().then(graficasBase64 => {
        const reporteData = {
            titulo,
            descripcion,
            tablas: tablasDatos,
            graficas: graficasBase64.filter(g => g !== null),
            csrfmiddlewaretoken: obtenerCSRFToken()
        };

        enviarReporteAlServidor(reporteData);
    });
}

function enviarReporteAlServidor(data) {
    // Ahora incluimos las gráficas en los datos enviados
    const datosConGraficas = {
        titulo: data.titulo,
        descripcion: data.descripcion,
        tablas: data.tablas,
        graficas: data.graficas, // Asegúrate de que esta línea coincide con cómo se almacenan tus gráficas
        csrfmiddlewaretoken: data.csrfmiddlewaretoken
    };

    //console.log("Datos que se enviarían incluyendo las gráficas:", datosConGraficas);
    //console.log(datosConGraficas.tablas);

    fetch('/report/exportar_reporte/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': obtenerCSRFToken()
        },
        body: JSON.stringify(datosConGraficas)
    })
    .then(response => {
        const contentType = response.headers.get("Content-Type");
        if (!response.ok) {
            if (contentType.includes("application/json")) {
                return response.json().then(errorData => {
                    console.error('Detalle del error:', errorData);
                    throw new Error(`La solicitud falló: ${response.statusText} - Código de estado: ${response.status}`);
                });
            } else {
                // Manejo de casos en los que la respuesta no es JSON
                return response.text().then(errorText => {
                    console.error('Respuesta de error no JSON:', errorText);
                    throw new Error(`La solicitud falló y no se devolvió JSON: ${response.statusText} - Código de estado: ${response.status}`);
                });
            }
        }
        return response.blob();
    })
    .then(data => {
        if (data instanceof Blob) {
            // Maneja la descarga del blob si la respuesta fue exitosa
            const url = window.URL.createObjectURL(data);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'reporte.docx';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();
        } // No se necesita un else aquí, ya que el caso de error lanza una excepción
    })
    .catch(error => {
        console.error('Error al exportar el reporte:', error);
        alert('Ocurrió un error al exportar el reporte. Verifica la consola para más detalles.');
    });
}