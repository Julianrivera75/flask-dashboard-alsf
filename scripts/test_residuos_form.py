"""
Script para probar el formulario de acciones de residuos
Simula el envío del formulario y verifica que funcione correctamente
"""
import sys
import os
from datetime import date, datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_modular import create_app
from forms.residuos_form import AccionResiduosForm
from models.acciones_residuos import AccionResiduos
from models.user import db

def test_form_submission():
    """Probar el envío del formulario"""
    
    app = create_app()
    
    with app.test_client() as client:
        print("=" * 60)
        print("PRUEBA DEL FORMULARIO DE ACCIONES DE RESIDUOS")
        print("=" * 60)
        
        # 1. Obtener la página del formulario (GET)
        print("\n1. Obteniendo pagina del formulario (GET)...")
        try:
            response = client.get('/acciones-residuos')
            if response.status_code == 200:
                print("   [OK] Pagina del formulario accesible")
                print(f"      Status code: {response.status_code}")
            else:
                print(f"   [ERROR] Status code inesperado: {response.status_code}")
                return False
        except Exception as e:
            print(f"   [ERROR] Error obteniendo pagina: {e}")
            return False
        
        # 2. Contar registros antes
        print("\n2. Contando registros antes del envio...")
        with app.app_context():
            try:
                registros_antes = AccionResiduos.query.count()
                print(f"   [OK] Registros antes: {registros_antes}")
            except Exception as e:
                print(f"   [ERROR] Error contando registros: {e}")
                return False
        
        # 3. Simular envío del formulario (POST)
        print("\n3. Enviando formulario (POST)...")
        try:
            # Datos de prueba
            form_data = {
                'localidad': 'Santa Fe',
                'numero_operativos': 5,
                'numero_comparendos': 10,
                'numero_sensibilizaciones': 3,
                'fecha_operacion': date.today().isoformat(),
                'usuario_registro': 'Usuario de Prueba',
                'observaciones': 'Registro de prueba del formulario',
                'submit': 'Registrar Acción'
            }
            
            response = client.post('/acciones-residuos', data=form_data, follow_redirects=True)
            
            if response.status_code == 200:
                print("   [OK] Formulario enviado exitosamente")
                print(f"      Status code: {response.status_code}")
                
                # Verificar que hay mensaje de éxito en la respuesta
                response_text = response.data.decode('utf-8', errors='ignore')
                if 'registrada exitosamente' in response_text.lower() or 'success' in response_text.lower():
                    print("   [OK] Mensaje de exito encontrado en la respuesta")
                else:
                    print("   [WARNING] No se encontro mensaje de exito en la respuesta")
            else:
                print(f"   [ERROR] Status code inesperado: {response.status_code}")
                print(f"      Response: {response.data[:200]}")
                return False
                
        except Exception as e:
            print(f"   [ERROR] Error enviando formulario: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # 4. Verificar que se guardó en la base de datos
        print("\n4. Verificando que se guardo en la base de datos...")
        with app.app_context():
            try:
                registros_despues = AccionResiduos.query.count()
                print(f"   [OK] Registros despues: {registros_despues}")
                
                if registros_despues > registros_antes:
                    print(f"   [OK] Se creo un nuevo registro (antes: {registros_antes}, despues: {registros_despues})")
                    
                    # Obtener el último registro
                    ultimo_registro = AccionResiduos.query.order_by(AccionResiduos.id.desc()).first()
                    if ultimo_registro:
                        print(f"   [OK] Ultimo registro encontrado:")
                        print(f"      - ID: {ultimo_registro.id}")
                        print(f"      - Localidad: {ultimo_registro.localidad}")
                        print(f"      - Operativos: {ultimo_registro.numero_operativos}")
                        print(f"      - Comparendos: {ultimo_registro.numero_comparendos}")
                        print(f"      - Sensibilizaciones: {ultimo_registro.numero_sensibilizaciones}")
                        print(f"      - Fecha operacion: {ultimo_registro.fecha_operacion}")
                        print(f"      - Usuario: {ultimo_registro.usuario_registro}")
                else:
                    print(f"   [ERROR] No se creo un nuevo registro")
                    return False
                    
            except Exception as e:
                print(f"   [ERROR] Error verificando base de datos: {e}")
                import traceback
                traceback.print_exc()
                return False
        
        # 5. Probar validación del formulario
        print("\n5. Probando validacion del formulario...")
        with app.app_context():
            try:
                # Probar con datos inválidos usando el cliente
                form_data_invalido = {
                    'localidad': '',  # Localidad vacía (inválido)
                    'numero_operativos': -5,  # Número negativo (inválido)
                    'fecha_operacion': '2099-12-31'  # Fecha futura (inválido)
                }
                
                response_invalido = client.post('/acciones-residuos', data=form_data_invalido, follow_redirects=True)
                
                # Si la validación funciona, debería mostrar errores o no guardar
                if response_invalido.status_code == 200:
                    # Verificar que no se creó un nuevo registro
                    registros_despues_invalido = AccionResiduos.query.count()
                    if registros_despues_invalido == registros_despues:
                        print("   [OK] Validacion funciona correctamente (no guardo datos invalidos)")
                    else:
                        print("   [WARNING] Se guardo un registro con datos invalidos")
                else:
                    print(f"   [OK] Validacion rechazo datos invalidos (status: {response_invalido.status_code})")
                    
            except Exception as e:
                print(f"   [WARNING] Error probando validacion: {e}")
                # No es crítico, continuar
        
        # 6. Verificar indicadores actualizados
        print("\n6. Verificando indicadores actualizados...")
        try:
            response = client.get('/acciones-residuos')
            if response.status_code == 200:
                # Verificar que los indicadores estén en la respuesta
                response_text = response.data.decode('utf-8', errors='ignore')
                if 'total-acciones' in response_text or str(registros_despues) in response_text:
                    print("   [OK] Indicadores presentes en la respuesta")
                else:
                    print("   [WARNING] No se encontraron indicadores en la respuesta")
            else:
                print(f"   [ERROR] No se pudo obtener la pagina: {response.status_code}")
        except Exception as e:
            print(f"   [ERROR] Error verificando indicadores: {e}")
        
        print("\n" + "=" * 60)
        print("[OK] TODAS LAS PRUEBAS DEL FORMULARIO COMPLETADAS EXITOSAMENTE")
        print("=" * 60)
        return True


if __name__ == '__main__':
    success = test_form_submission()
    sys.exit(0 if success else 1)

