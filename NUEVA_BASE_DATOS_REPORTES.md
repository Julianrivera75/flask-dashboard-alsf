# 🗄️ Nueva Base de Datos para Reportes ALSF

## 📋 **Configuración Implementada**

### **Base de Datos Separadas:**

**Base de Datos 1: "1000 Acciones en 1 Día"**
- 🔗 **Variable:** `DATABASE_URL`
- 📊 **Tablas:** `actividades_1000`, `fotos_actividades_1000`
- 🎯 **Propósito:** Programa especial de 1000 acciones

**Base de Datos 2: "Reportes ALSF" (NUEVA)**
- 🔗 **Variable:** `REPORTES_DATABASE_URL`
- 📊 **Tablas:** `reportes`, `responsables`, `tipos_actividad`, `entidades`, `sectores`
- 🎯 **Propósito:** Reportes administrativos diarios

## 🚀 **Pasos para Implementar en Railway**

### **Paso 1: Crear Nueva Base de Datos**
1. **Ir a Railway Dashboard**
2. **Click "New" → "Database" → "PostgreSQL"**
3. **Nombre:** `alsf-reportes-database`
4. **Railway creará automáticamente la BD**

### **Paso 2: Configurar Variables de Entorno**
1. **Click en tu servicio de aplicación Flask**
2. **Ir a "Variables"**
3. **Agregar nueva variable:**
   - **Nombre:** `REPORTES_DATABASE_URL`
   - **Valor:** Copiar el valor de `DATABASE_URL` de la nueva BD

### **Paso 3: Verificar Configuración**
**Variables que deben estar configuradas:**
- ✅ `DATABASE_URL` → Para "1000 acciones" (existente)
- ✅ `REPORTES_DATABASE_URL` → Para "Reportes ALSF" (nueva)
- ✅ `SECRET_KEY` → Clave secreta de la aplicación

## 📊 **Estructura de la Nueva Base de Datos**

### **Tablas que se Crearán Automáticamente:**

**1. `responsables` (47 registros)**
- Personal ALSF completo
- Nombres y apellidos
- Estado activo/inactivo

**2. `tipos_actividad` (21 registros)**
- Estrategias y operativos
- Actividades de monitoreo
- Reuniones y acompañamientos

**3. `entidades` (14 registros)**
- ALSF, MEBOG, IPES
- Secretarías distritales
- Entidades participantes

**4. `sectores` (22 registros)**
- Localidades de Bogotá
- Centro Histórico, Chapinero, Santa Fe
- Orden y estado activo

**5. `reportes` (dinámico)**
- Formularios enviados
- Fecha, responsable, coordenadas
- Tipo de actividad, sector

**6. `resultados_reporte` (dinámico)**
- Datos específicos de actividades
- Cambuches, armas, requisas
- Sellamientos, sensibilizaciones

**7. `archivos_reporte` (dinámico)**
- Fotos antes/después
- Documentos PDF
- Nombres y rutas de archivos

**8. `users` (1 registro)**
- Usuario administrador
- Email: admin@alsf.gov.co
- Contraseña: ALSF2025

## 🔧 **Scripts de Inicialización**

### **Script Principal:**
- **Archivo:** `scripts/init_reportes_database.py`
- **Función:** Cargar todos los datos básicos
- **Ejecución:** Automática al iniciar la aplicación

### **Datos que se Cargarán:**
- ✅ 47 Responsables ALSF
- ✅ 21 Tipos de actividad
- ✅ 14 Entidades participantes
- ✅ 22 Sectores de Bogotá
- ✅ 1 Usuario administrador

## 🎯 **Ventajas de la Nueva Configuración**

### **Separación Clara:**
- ✅ **Funcionalidades independientes**
- ✅ **Bases de datos separadas**
- ✅ **Mantenimiento independiente**

### **Escalabilidad:**
- ✅ **Crecimiento independiente**
- ✅ **Backup separado**
- ✅ **Permisos diferentes**

### **Mantenimiento:**
- ✅ **Fácil gestión**
- ✅ **Debugging independiente**
- ✅ **Actualizaciones separadas**

## 🚨 **Verificación Post-Implementación**

### **Después de desplegar, verificar:**

1. **Railway Dashboard:**
   - ✅ Dos servicios PostgreSQL
   - ✅ Variables configuradas
   - ✅ Servicios "Running"

2. **Aplicación:**
   - ✅ Formulario de reportes carga opciones
   - ✅ Formulario 1000 acciones sigue funcionando
   - ✅ Login funciona correctamente

3. **Base de Datos:**
   - ✅ Tablas creadas automáticamente
   - ✅ Datos básicos cargados
   - ✅ Usuario admin disponible

## 📝 **Comandos de Verificación**

### **Ver tablas creadas:**
```sql
-- En la nueva base de datos de reportes
\dt
```

### **Ver datos cargados:**
```sql
-- Contar registros por tabla
SELECT 'responsables' as tabla, COUNT(*) as total FROM responsables
UNION ALL
SELECT 'tipos_actividad', COUNT(*) FROM tipos_actividad
UNION ALL
SELECT 'entidades', COUNT(*) FROM entidades
UNION ALL
SELECT 'sectores', COUNT(*) FROM sectores;
```

### **Verificar usuario admin:**
```sql
-- Ver usuario administrador
SELECT email, first_name, last_name, role FROM users;
```

## 🎉 **Resultado Final**

**Después de implementar:**
- ✅ **Formulario de reportes** funcionará con todas las opciones
- ✅ **Formulario 1000 acciones** seguirá funcionando
- ✅ **Bases de datos separadas** y organizadas
- ✅ **Sistema escalable** y mantenible

---

**Estado:** ✅ **CONFIGURACIÓN COMPLETA**  
**Fecha:** 3 de septiembre de 2025  
**Próximo paso:** Desplegar a Railway





