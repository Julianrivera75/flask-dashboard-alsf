# 🚀 Guía Completa de Supabase para ALSF

## 📋 **Paso 1: Crear Cuenta**

1. **Ir a [supabase.com](https://supabase.com)**
2. **Click en "Start your project"**
3. **Conectar con GitHub** (recomendado)
4. **Crear nuevo proyecto**

## 🏗️ **Paso 2: Configurar Proyecto**

### **A. Información del Proyecto:**
- **Nombre**: `alsf-reports`
- **Database Password**: `tu_password_seguro_2024`
- **Region**: `us-east-1` (más cercano a Colombia)

### **B. Esperar Configuración:**
- ⏱️ **2-3 minutos** para crear la base de datos
- ✅ **URL del proyecto**: `https://alsf-reports.supabase.co`
- ✅ **API Key**: Se genera automáticamente

## 🗄️ **Paso 3: Crear Tabla de Reportes**

### **A. Ir a SQL Editor:**
1. **Dashboard** → **SQL Editor**
2. **New Query**

### **B. Ejecutar Script SQL:**

```sql
-- Crear tabla de reportes
CREATE TABLE reportes (
    id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefono VARCHAR(50),
    organizacion VARCHAR(255),
    direccion TEXT NOT NULL,
    latitud DECIMAL(10, 8) NOT NULL,
    longitud DECIMAL(11, 8) NOT NULL,
    tipo_reporte VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    prioridad VARCHAR(50) DEFAULT 'media',
    fecha_reporte DATE,
    hora_reporte TIME,
    fotos_urls TEXT[],
    timestamp TIMESTAMP DEFAULT NOW(),
    user_agent TEXT,
    estado VARCHAR(50) DEFAULT 'pendiente',
    fecha_actualizacion TIMESTAMP,
    
    -- Índices para búsquedas rápidas
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT valid_coordinates CHECK (
        latitud BETWEEN -90 AND 90 AND 
        longitud BETWEEN -180 AND 180
    )
);

-- Crear índices para optimizar consultas
CREATE INDEX idx_reportes_tipo ON reportes(tipo_reporte);
CREATE INDEX idx_reportes_estado ON reportes(estado);
CREATE INDEX idx_reportes_fecha ON reportes(fecha_reporte);
CREATE INDEX idx_reportes_coords ON reportes(latitud, longitud);
CREATE INDEX idx_reportes_timestamp ON reportes(timestamp DESC);

-- Crear tabla de estadísticas (opcional)
CREATE TABLE estadisticas_reportes (
    id BIGSERIAL PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    total_reportes INTEGER DEFAULT 0,
    reportes_por_tipo JSONB,
    reportes_por_prioridad JSONB,
    reportes_por_estado JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Función para actualizar estadísticas automáticamente
CREATE OR REPLACE FUNCTION actualizar_estadisticas()
RETURNS TRIGGER AS $$
BEGIN
    -- Actualizar estadísticas diarias
    INSERT INTO estadisticas_reportes (
        total_reportes,
        reportes_por_tipo,
        reportes_por_prioridad,
        reportes_por_estado
    )
    SELECT 
        COUNT(*),
        jsonb_object_agg(tipo_reporte, count) as tipos,
        jsonb_object_agg(prioridad, count) as prioridades,
        jsonb_object_agg(estado, count) as estados
    FROM (
        SELECT 
            tipo_reporte,
            prioridad,
            estado,
            COUNT(*) as count
        FROM reportes 
        WHERE DATE(timestamp) = CURRENT_DATE
        GROUP BY tipo_reporte, prioridad, estado
    ) stats
    ON CONFLICT (fecha) DO UPDATE SET
        total_reportes = EXCLUDED.total_reportes,
        reportes_por_tipo = EXCLUDED.reportes_por_tipo,
        reportes_por_prioridad = EXCLUDED.reportes_por_prioridad,
        reportes_por_estado = EXCLUDED.reportes_por_estado;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para actualizar estadísticas automáticamente
CREATE TRIGGER trigger_actualizar_estadisticas
    AFTER INSERT OR UPDATE OR DELETE ON reportes
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_estadisticas();
```

## 🔐 **Paso 4: Configurar Autenticación (Opcional)**

### **A. Habilitar Auth:**
1. **Authentication** → **Settings**
2. **Enable Email Auth**
3. **Configurar templates de email**

### **B. Configurar RLS (Row Level Security):**

```sql
-- Habilitar RLS en la tabla
ALTER TABLE reportes ENABLE ROW LEVEL SECURITY;

-- Política para permitir inserción pública
CREATE POLICY "Permitir inserción pública" ON reportes
    FOR INSERT WITH CHECK (true);

-- Política para lectura (solo reportes públicos)
CREATE POLICY "Permitir lectura pública" ON reportes
    FOR SELECT USING (estado != 'privado');

-- Política para administradores
CREATE POLICY "Acceso completo para admins" ON reportes
    FOR ALL USING (auth.role() = 'authenticated');
```

## 📡 **Paso 5: Configurar API**

### **A. Obtener Credenciales:**
1. **Settings** → **API**
2. **Project URL**: `https://alsf-reports.supabase.co`
3. **anon public key**: `tu-anon-key`
4. **service_role key**: `tu-service-key` (mantener secreto)

### **B. Variables de Entorno:**
```bash
SUPABASE_URL=https://alsf-reports.supabase.co
SUPABASE_ANON_KEY=tu-anon-key
SUPABASE_SERVICE_KEY=tu-service-key
```

## 🗂️ **Paso 6: Configurar Almacenamiento (Fotos)**

### **A. Crear Bucket:**
1. **Storage** → **New Bucket**
2. **Nombre**: `reportes-fotos`
3. **Public**: ✅ (para acceso directo)

### **B. Configurar Políticas:**
```sql
-- Permitir subir fotos
CREATE POLICY "Permitir subir fotos" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'reportes-fotos');

-- Permitir ver fotos públicas
CREATE POLICY "Permitir ver fotos" ON storage.objects
    FOR SELECT USING (bucket_id = 'reportes-fotos');
```

## 🔄 **Paso 7: Configurar Tiempo Real (Opcional)**

### **A. Habilitar Realtime:**
1. **Database** → **Replication**
2. **Enable** para tabla `reportes`

### **B. Suscripción en Frontend:**
```javascript
// Suscribirse a nuevos reportes
const subscription = supabase
    .from('reportes')
    .on('INSERT', payload => {
        console.log('Nuevo reporte:', payload.new);
        // Actualizar UI en tiempo real
    })
    .subscribe();
```

## 📊 **Paso 8: Crear Vistas y Funciones**

### **A. Vista de Reportes Recientes:**
```sql
CREATE VIEW reportes_recientes AS
SELECT 
    id,
    nombre,
    tipo_reporte,
    prioridad,
    estado,
    fecha_reporte,
    latitud,
    longitud,
    direccion
FROM reportes 
WHERE timestamp >= NOW() - INTERVAL '7 days'
ORDER BY timestamp DESC;
```

### **B. Función para Estadísticas:**
```sql
CREATE OR REPLACE FUNCTION obtener_estadisticas()
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'total_reportes', COUNT(*),
        'por_tipo', json_object_agg(tipo_reporte, count),
        'por_prioridad', json_object_agg(prioridad, count),
        'por_estado', json_object_agg(estado, count),
        'recientes', json_agg(
            json_build_object(
                'id', id,
                'nombre', nombre,
                'tipo', tipo_reporte,
                'fecha', fecha_reporte
            )
        )
    ) INTO result
    FROM (
        SELECT 
            tipo_reporte,
            prioridad,
            estado,
            COUNT(*) as count,
            id,
            nombre,
            fecha_reporte
        FROM reportes 
        GROUP BY tipo_reporte, prioridad, estado, id, nombre, fecha_reporte
        ORDER BY fecha_reporte DESC
        LIMIT 10
    ) stats;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;
```

## 🧪 **Paso 9: Probar la Configuración**

### **A. Insertar Datos de Prueba:**
```sql
INSERT INTO reportes (
    nombre, email, direccion, latitud, longitud, 
    tipo_reporte, descripcion, prioridad
) VALUES (
    'Juan Pérez',
    'juan@example.com',
    'Calle 123, Bogotá',
    4.7110,
    -74.0721,
    'infraestructura',
    'Bache en la calle principal',
    'alta'
);
```

### **B. Verificar Datos:**
```sql
SELECT * FROM reportes ORDER BY timestamp DESC LIMIT 5;
```

## 🔧 **Paso 10: Integración con Flask**

### **A. Instalar Dependencias:**
```bash
pip install supabase
```

### **B. Configurar en tu App:**
```python
from supabase import create_client, Client

url = "https://alsf-reports.supabase.co"
key = "tu-anon-key"
supabase: Client = create_client(url, key)
```

## 📈 **Monitoreo y Análisis:**

### **A. Dashboard de Supabase:**
- **Database**: Ver tablas y datos
- **Logs**: Monitorear consultas
- **Analytics**: Métricas de uso

### **B. Alertas Recomendadas:**
- **80%** de uso de almacenamiento
- **90%** de uso de base de datos
- **Errores** de API

## 🚨 **Mejores Prácticas:**

### **✅ Hacer:**
- ✅ **Usar índices** para consultas frecuentes
- ✅ **Validar datos** en la base de datos
- ✅ **Configurar RLS** para seguridad
- ✅ **Monitorear uso** de recursos

### **❌ Evitar:**
- ❌ **No exponer** service_role key
- ❌ **No hacer** consultas sin límites
- ❌ **No subir** archivos muy grandes
- ❌ **No olvidar** configurar backups

## 💡 **Ventajas para tu Proyecto:**

| Aspecto | Supabase | Google Sheets | Firebase |
|---------|----------|---------------|----------|
| **Base de Datos** | PostgreSQL | Hojas de cálculo | Firestore |
| **Geolocalización** | ✅ Nativa | ❌ Manual | ✅ Nativa |
| **API** | ✅ Automática | ❌ Limitada | ✅ Automática |
| **Tiempo Real** | ✅ Incluido | ❌ No | ✅ Incluido |
| **Escalabilidad** | ✅ Alta | ❌ Limitada | ✅ Alta |
| **Costo** | ✅ Gratis | ✅ Gratis | ⚠️ Limitado |

¿Te gustaría que te ayude a configurar Supabase paso a paso para tu proyecto? 