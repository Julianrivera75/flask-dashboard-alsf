// Funciones específicas para gráficos y visualizaciones

// Función para actualizar todos los visualizadores
function updateVisualizadores(data) {
    console.log('🎨 Iniciando actualización de visualizadores...');
    console.log('📊 Datos recibidos en updateVisualizadores:', data);
    
    if (!data || data.length === 0) {
        console.log('❌ No hay datos para actualizar visualizadores');
        return;
    }
    
    console.log('✅ Datos válidos, procediendo con actualizaciones...');
    
    // Mostrar información de debugging en la interfaz
    mostrarInfoDebugging(data);
    
    // Actualizar indicadores
    console.log('📊 Actualizando indicadores...');
    updateIndicadores(data);
    
    // Actualizar gráfica de participación
    console.log('📈 Actualizando gráfica de participación...');
    updateParticipacionChart(data);
    
    // Actualizar gráfica de participación diaria
    console.log('📅 Llamando a updateParticipacionDiariaChart...');
    console.log('📊 Datos que se pasarán a updateParticipacionDiariaChart:', data.length, 'registros');
    updateParticipacionDiariaChart(data);
    console.log('✅ updateParticipacionDiariaChart llamada exitosamente');
    
    console.log('✅ Actualización de visualizadores completada');
}

// Función para mostrar información de debugging
function mostrarInfoDebugging(data) {
    console.log(`\n🔍 ANÁLISIS COMPLETO DE DATOS:`);
    console.log(`   📊 Total de registros: ${data.length}`);
    
    if (data.length > 0) {
        console.log(`   📋 Columnas disponibles: ${Object.keys(data[0]).join(', ')}`);
        
        // Analizar columna de fechas
        const columnaFecha = 'Fecha final de ejecución';
        if (columnaFecha in data[0]) {
            console.log(`   📅 Columna de fecha encontrada: "${columnaFecha}"`);
            
            // Mostrar algunas fechas de ejemplo
            const fechasEjemplo = data.slice(0, 5).map(row => row[columnaFecha]);
            console.log(`   📝 Primeras 5 fechas:`, fechasEjemplo);
        } else {
            console.log(`   ❌ Columna de fecha no encontrada: "${columnaFecha}"`);
            console.log(`   🔍 Buscando columnas similares...`);
            const columnasSimilares = Object.keys(data[0]).filter(col => 
                col.toLowerCase().includes('fecha') || 
                col.toLowerCase().includes('date') ||
                col.toLowerCase().includes('ejecución')
            );
            console.log(`   📋 Columnas similares encontradas:`, columnasSimilares);
        }
    }
}

// Función para actualizar indicadores
function updateIndicadores(data) {
    // Calcular población impactada
    let poblacionTotal = 0;
    let fechasValidas = 0;
    let fechasInvalidas = 0;
    
    data.forEach(row => {
        const poblacion = parseFloat(row['Población impactada']) || 0;
        poblacionTotal += poblacion;
        
        // Contar fechas válidas e inválidas
        const fecha = row['Fecha final de ejecución'];
        if (fecha && fecha !== 'None' && fecha !== '' && fecha.match(/^\d{4}-\d{2}-\d{2}$/)) {
            try {
                const fechaObj = new Date(fecha);
                if (!isNaN(fechaObj.getTime())) {
                    fechasValidas++;
                } else {
                    fechasInvalidas++;
                }
            } catch (e) {
                fechasInvalidas++;
            }
        } else {
            fechasInvalidas++;
        }
    });
    
    document.getElementById('personas-impactadas').textContent = poblacionTotal.toLocaleString('es-CO');
    document.getElementById('actividades-realizadas').textContent = data.length.toString();
    
    // Mostrar información sobre fechas en consola
    console.log(`📅 Procesamiento de fechas:`);
    console.log(`   ✅ Fechas válidas: ${fechasValidas}`);
    console.log(`   ❌ Fechas inválidas: ${fechasInvalidas}`);
    console.log(`   📊 Total de registros: ${data.length}`);
    
    if (fechasInvalidas > 0) {
        console.log(`   ⚠️ ${((fechasInvalidas / data.length) * 100).toFixed(1)}% de fechas necesitan corrección`);
    }
}

// Función para actualizar gráfica de participación
function updateParticipacionChart(data) {
    // Lógica específica del gráfico de participación
    console.log('📊 Actualizando gráfico de participación...');
    
    // Aquí iría la lógica específica del gráfico de participación
    // Por ahora solo un log
}

// Función para actualizar tabla de datos
function updateDataTable(data) {
    if (!data || data.length === 0) return;
    
    fetch('/api/data').then(res => res.json()).then(json => {
        let headers = json.columns_order || Object.keys(data[0]);
        const tableHeaders = document.getElementById('table-headers');
        const tableBody = document.getElementById('table-body');
        
        tableHeaders.innerHTML = '';
        tableBody.innerHTML = '';
        
        headers.forEach((header, idx) => {
            const th = document.createElement('th');
            th.textContent = header;
            
            // Agregar botón de filtro para la columna "Entidad"
            if (header === 'Entidad') {
                const filterBtn = document.createElement('button');
                filterBtn.className = 'filter-btn';
                filterBtn.innerHTML = '<i class="fas fa-filter"></i>';
                filterBtn.onclick = () => showEntidadDropdown(th, data, headers);
                th.appendChild(filterBtn);
            }
            
            tableHeaders.appendChild(th);
        });
        
        data.forEach(row => {
            const tr = document.createElement('tr');
            headers.forEach(header => {
                const td = document.createElement('td');
                td.textContent = row[header] || '';
                tr.appendChild(td);
            });
            tableBody.appendChild(tr);
        });
        
        document.getElementById('data-table-container').style.display = 'block';
    });
}

// Exportar funciones para uso en otros archivos
window.updateVisualizadores = updateVisualizadores;
window.updateIndicadores = updateIndicadores;
window.updateParticipacionChart = updateParticipacionChart;
window.updateParticipacionDiariaChart = updateParticipacionDiariaChart;
window.updateDataTable = updateDataTable; 