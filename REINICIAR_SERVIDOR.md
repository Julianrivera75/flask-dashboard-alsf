# INSTRUCCIONES PARA REINICIAR EL SERVIDOR

## Problema: Los cambios en HTML no se reflejan

Si los cambios en el HTML no se ven, el servidor Flask no está recargando los templates.

## Solución RÁPIDA:

### Opción 1: Usar el script de reinicio (Windows)
```powershell
.\reiniciar_servidor.bat
```

### Opción 2: Reinicio manual

1. **Detener TODOS los procesos de Python:**
   ```powershell
   Get-Process python | Stop-Process -Force
   ```

2. **Limpiar caché de Python:**
   ```powershell
   Get-ChildItem -Path . -Filter __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force
   ```

3. **Reiniciar el servidor:**
   ```powershell
   python start_server.py
   ```

4. **Limpiar caché del navegador:**
   - Presiona `Ctrl + Shift + Delete`
   - O simplemente `Ctrl + F5` en la página

## Verificación:

1. Abre `http://localhost:5000/acciones-residuos`
2. Presiona `Ctrl + U` para ver el código fuente
3. Busca: "Registro de Acciones"
4. Si aparece, el servidor está funcionando correctamente

## Si aún no funciona:

1. Cierra TODAS las ventanas de terminal
2. Cierra el navegador completamente
3. Abre una nueva terminal
4. Ve al directorio del proyecto
5. Ejecuta: `python start_server.py`
6. Abre el navegador en modo incógnito (`Ctrl + Shift + N`)
7. Ve a: `http://localhost:5000/acciones-residuos`

