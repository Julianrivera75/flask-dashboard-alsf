// Script para verificar que ACTIVIDADES_DISPONIBLES tenga exactamente 32 elementos

// Array de actividades (copiado del archivo acciones_1000_common.js)
const ACTIVIDADES_DISPONIBLES = [
    'Diálogo diferencial LGBTI',
    'Fiesta Mayor',
    'Feria de Emprendedoras y Productoras Locales',
    'Recuperación entornos tramos universitarios - sector las aguas-',
    'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA',
    'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA', 'DANZA',
    'DANZA', 'DANZA', // Total: 22 DANZA
    'Jornada de embellecimiento',
    'Jornada de Protección y Bienestar Animal - PYBA',
    'MES MAYOR',
    'INAUGURACIÓN CENTRO DE EXPERIENCIA TIC',
    'Actividad',
    'Encuentro'
];

// Verificar el total
console.log('🔍 VERIFICANDO ARRAY DE ACTIVIDADES');
console.log('=' * 50);
console.log(`Total de elementos: ${ACTIVIDADES_DISPONIBLES.length}`);

if (ACTIVIDADES_DISPONIBLES.length === 32) {
    console.log('✅ CORRECTO: El array tiene exactamente 32 elementos');
} else {
    console.log(`❌ INCORRECTO: El array tiene ${ACTIVIDADES_DISPONIBLES.length} elementos, debería tener 32`);
}

// Contar DANZA específicamente
const danzaCount = ACTIVIDADES_DISPONIBLES.filter(act => act === 'DANZA').length;
console.log(`DANZA aparece: ${danzaCount} veces`);

// Listar todas las actividades únicas
const actividadesUnicas = [...new Set(ACTIVIDADES_DISPONIBLES)];
console.log(`Actividades únicas: ${actividadesUnicas.length}`);
console.log('Actividades únicas:', actividadesUnicas);

console.log('=' * 50);

