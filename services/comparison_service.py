#!/usr/bin/env python3
"""
Script de comparación entre la versión procedural y la versión POO
"""

def compare_architectures():
    """Compara las dos arquitecturas del proyecto"""
    
    print("🏗️ COMPARACIÓN DE ARQUITECTURAS")
    print("=" * 50)
    
    # Comparación de archivos
    print("\n📁 ESTRUCTURA DE ARCHIVOS:")
    print("-" * 30)
    
    print("🔴 VERSIÓN PROCEDURAL (Original):")
    print("   ├── app.py (281 líneas)")
    print("   ├── templates/index.html")
    print("   └── requirements.txt")
    
    print("\n🟢 VERSIÓN POO (Nueva):")
    print("   ├── app_oop.py (150 líneas)")
    print("   ├── data_manager.py (200 líneas)")
    print("   ├── google_sheets_connector.py (70 líneas)")
    print("   ├── chart_generator.py (180 líneas)")
    print("   ├── config.py (50 líneas)")
    print("   ├── templates/index.html")
    print("   └── requirements.txt")
    
    # Comparación de responsabilidades
    print("\n🎯 SEPARACIÓN DE RESPONSABILIDADES:")
    print("-" * 40)
    
    print("🔴 VERSIÓN PROCEDURAL:")
    print("   ❌ Todo en un solo archivo")
    print("   ❌ Funciones mezcladas")
    print("   ❌ Configuración dispersa")
    print("   ❌ Difícil mantenimiento")
    
    print("\n🟢 VERSIÓN POO:")
    print("   ✅ BogotaApp: Coordinación general")
    print("   ✅ DataManager: Gestión de datos")
    print("   ✅ GoogleSheetsConnector: Conexión externa")
    print("   ✅ ChartGenerator: Visualizaciones")
    print("   ✅ Config: Configuración centralizada")
    
    # Ventajas de POO
    print("\n🚀 VENTAJAS DE LA ARQUITECTURA POO:")
    print("-" * 40)
    
    advantages = [
        "📈 Mantenibilidad: Cambios localizados y controlados",
        "🔧 Escalabilidad: Fácil agregar nuevas funcionalidades",
        "🧪 Testabilidad: Cada clase se puede probar independientemente",
        "♻️ Reutilización: Componentes reutilizables en otros proyectos",
        "👥 Colaboración: Mejor división de trabajo entre desarrolladores",
        "📖 Legibilidad: Código más organizado y fácil de entender",
        "🛡️ Robustez: Mejor manejo de errores y excepciones",
        "⚙️ Configuración: Centralizada y fácil de modificar"
    ]
    
    for advantage in advantages:
        print(f"   {advantage}")
    
    # Métricas de código
    print("\n📊 MÉTRICAS DE CÓDIGO:")
    print("-" * 25)
    
    print("🔴 VERSIÓN PROCEDURAL:")
    print("   📏 Líneas totales: 281")
    print("   🔗 Acoplamiento: Alto")
    print("   🎯 Cohesión: Baja")
    print("   🧪 Testabilidad: Difícil")
    
    print("\n🟢 VERSIÓN POO:")
    print("   📏 Líneas totales: 650 (distribuidas)")
    print("   🔗 Acoplamiento: Bajo")
    print("   🎯 Cohesión: Alta")
    print("   🧪 Testabilidad: Fácil")
    
    # Funcionalidades mantenidas
    print("\n✅ FUNCIONALIDADES MANTENIDAS:")
    print("-" * 35)
    
    features = [
        "🌐 Dashboard web completo",
        "📊 Gráfico de pie por entidad",
        "📅 Gráfico diario de actividades",
        "📈 Gráfico mensual por entidad",
        "🏆 Top 3 de entidades",
        "📊 Indicadores en tiempo real",
        "🔄 Actualización automática",
        "🔄 Actualización manual",
        "📅 Normalización de fechas",
        "🔢 Cálculo de indicadores",
        "🔐 Reseteo de contadores",
        "📋 Resúmenes por entidad"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    # Instrucciones de uso
    print("\n🚀 CÓMO USAR:")
    print("-" * 15)
    
    print("🔴 Versión Procedural:")
    print("   python app.py")
    
    print("\n🟢 Versión POO:")
    print("   python app_oop.py")
    
    print("\n💡 RECOMENDACIÓN:")
    print("   Usar la versión POO para desarrollo y mantenimiento")
    print("   Mantener la versión procedural como respaldo")

if __name__ == "__main__":
    compare_architectures() 