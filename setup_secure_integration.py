#!/usr/bin/env python3
"""
Setup Seguro para HallBayes + IntegridAI Integration
Configuración automática con protección de API keys
"""

import os
import sys
import getpass
import shutil
from pathlib import Path

def create_secure_env():
    """Crea archivo .env de forma segura"""
    
    print("🔐 Configuración Segura de HallBayes + IntegridAI")
    print("=" * 50)
    
    # Verificar si ya existe .env
    env_path = Path(".env")
    if env_path.exists():
        response = input("❓ .env ya existe. ¿Sobrescribir? (y/N): ")
        if response.lower() != 'y':
            print("🚫 Configuración cancelada")
            return False
    
    # Solicitar API key de forma segura
    print("\\n🔑 Configuración de API Keys:")
    print("💡 Tu API key no será mostrada en pantalla")
    
    api_key = getpass.getpass("OpenAI API Key (sk-proj-...): ")
    
    if not api_key:
        print("⚠️  API key vacía. ¿Continuar en modo demo? (y/N): ")
        if input().lower() != 'y':
            return False
        api_key = ""
    
    # Validar formato de API key
    if api_key and not api_key.startswith(('sk-', 'sk-proj-')):
        print("❌ Formato de API key incorrecto")
        return False
    
    # Configuración adicional
    print("\\n⚙️  Configuración Adicional:")
    
    model = input("Modelo OpenAI (gpt-4o-mini): ") or "gpt-4o-mini"
    threshold = input("Threshold de abstención (0.05): ") or "0.05"
    debug = input("Modo debug (false): ") or "false"
    
    # Crear contenido .env
    env_content = f"""# Configuración HallBayes + IntegridAI
# Generado automáticamente - NO COMMITEAR ESTE ARCHIVO

# OpenAI Configuration
OPENAI_API_KEY={api_key}
HALLBAYES_MODEL={model}
HALLBAYES_TEMPERATURE=0.3
HALLBAYES_ABSTENTION_THRESHOLD={threshold}
HALLBAYES_MAX_COST_PER_QUERY=0.05

# IntegridAI Configuration  
INTEGRIDAI_DSP_TAU=0.8
INTEGRIDAI_CULTURAL_FACTOR=1.2
INTEGRIDAI_LEGAL_MODE=true

# System Configuration
DEBUG_MODE={debug}
LOG_LEVEL=INFO
ENABLE_AUDIT_TRAIL=true
MASK_API_KEYS=true
MAX_RETRIES=3

# Security
HALLBAYES_CACHING=true
"""
    
    # Escribir archivo .env
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        
        # Establecer permisos seguros
        os.chmod(".env", 0o600)  # Solo lectura/escritura para propietario
        
        print("✅ Archivo .env creado con permisos seguros")
        
        # Verificar que .env está en .gitignore
        ensure_gitignore()
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando .env: {e}")
        return False

def ensure_gitignore():
    """Asegura que .env esté en .gitignore"""
    
    gitignore_path = Path(".gitignore")
    env_in_gitignore = False
    
    if gitignore_path.exists():
        with open(".gitignore", "r") as f:
            content = f.read()
            if ".env" in content:
                env_in_gitignore = True
    
    if not env_in_gitignore:
        with open(".gitignore", "a") as f:
            f.write("\\n# Environment variables\\n.env\\n")
        print("✅ .env añadido a .gitignore")

def install_dependencies():
    """Instala dependencias requeridas"""
    
    print("\\n📦 Instalando dependencias...")
    
    dependencies = [
        "openai>=1.0.0",
        "python-dotenv",
        "asyncio",
        "dataclasses-json"
    ]
    
    try:
        import subprocess
        for dep in dependencies:
            print(f"  📦 Instalando {dep}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                                 capture_output=True, text=True)
            if result.returncode != 0:
                print(f"⚠️  Error instalando {dep}: {result.stderr}")
            else:
                print(f"  ✅ {dep} instalado")
                
        return True
        
    except Exception as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def test_configuration():
    """Prueba la configuración"""
    
    print("\\n🧪 Probando configuración...")
    
    try:
        # Importar y probar configuración
        sys.path.append("hallbayes-integration")
        from config import config_manager
        
        # Validar configuración
        if config_manager.validate_configuration():
            print("✅ Configuración validada correctamente")
        else:
            print("⚠️  Configuración en modo demo (sin API key)")
        
        # Probar motor principal
        from certified_compliance_engine import CertifiedComplianceEngine
        
        engine = CertifiedComplianceEngine()
        report = engine.get_system_report()
        
        print("\\n📊 Estado del Sistema:")
        print(f"  HallBayes: {'✅ Habilitado' if report['system_status']['hallbayes_enabled'] else '⚠️  Demo Mode'}")
        print(f"  IntegridAI: {'✅ Habilitado' if report['system_status']['integridai_enabled'] else '❌ No disponible'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando configuración: {e}")
        return False

def main():
    """Función principal de configuración"""
    
    print("🚀 Setup de HallBayes + IntegridAI Integration")
    print("============================================")
    
    # Verificar directorio
    if not os.path.exists("hallbayes-integration"):
        print("❌ Directorio hallbayes-integration no encontrado")
        print("💡 Ejecutar desde el directorio integridai-hackai-2025/")
        return
    
    # Pasos de configuración
    steps = [
        ("🔐 Configurar variables de entorno", create_secure_env),
        ("📦 Instalar dependencias", install_dependencies), 
        ("🧪 Probar configuración", test_configuration)
    ]
    
    for step_name, step_func in steps:
        print(f"\\n{step_name}...")
        if not step_func():
            print(f"❌ Error en: {step_name}")
            return
    
    print("\\n🎉 ¡CONFIGURACIÓN COMPLETADA!")
    print("=" * 30)
    print("✅ Sistema HallBayes + IntegridAI listo")
    print("🔐 API keys protegidas con permisos 600")
    print("📝 .env añadido a .gitignore")
    print("🧪 Configuración validada")
    
    print("\\n🚀 Próximos pasos:")
    print("1. cd hallbayes-integration")
    print("2. python certified_compliance_engine.py")
    print("3. ¡Usar compliance certificado!")
    
    print("\\n⚠️  SEGURIDAD:")
    print("- NUNCA comitear el archivo .env")
    print("- Rotar API keys regularmente") 
    print("- Monitorear uso de OpenAI API")

if __name__ == "__main__":
    main()