# INSTRUCCIONES PARA VER LOS CAMBIOS

## El orden en el código es CORRECTO:
1. Indicadores (Acciones Registradas y Puntos de Intervención)
2. Mapa de Localidades  
3. Formulario de Registro (debajo del mapa)

## Si no ves los cambios, sigue estos pasos:

### PASO 1: Detener TODOS los procesos de Python
```powershell
# En PowerShell, ejecuta:
Get-Process python | Stop-Process -Force
```

### PASO 2: Limpiar caché de Python
```powershell
# Eliminar archivos __pycache__
Get-ChildItem -Path . -Filter __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force
```

### PASO 3: Reiniciar el servidor
```powershell
python start_server.py
```

### PASO 4: Limpiar caché del navegador
1. Abre el navegador
2. Presiona `Ctrl + Shift + Delete`
3. Selecciona "Caché" o "Cached images and files"
4. Haz clic en "Borrar datos"
5. O simplemente presiona `Ctrl + F5` en la página

### PASO 5: Verificar en el código fuente
1. Abre la página en el navegador
2. Presiona `Ctrl + U` para ver el código fuente
3. Busca: "FORMULARIO DE REGISTRO - VERSIÓN ACTUALIZADA"
4. Si NO aparece, el servidor no está recargando

### PASO 6: Verificar en la consola del navegador
1. Presiona `F12` para abrir las herramientas de desarrollador
2. Ve a la pestaña "Network" (Red)
3. Recarga la página (`F5`)
4. Busca el archivo `acciones_residuos.html`
5. Verifica que la fecha/hora sea reciente

## Si aún no funciona:
- Verifica que estés accediendo a: `http://localhost:5000/acciones-residuos`
- Verifica que no haya múltiples servidores corriendo en diferentes puertos
- Intenta acceder en modo incógnito (`Ctrl + Shift + N`)

