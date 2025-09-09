#!/usr/bin/env python3
"""
Configuración segura para HallBayes + IntegridAI Integration
Manejo de API keys y configuración sin exponer datos sensibles
"""

import os
from dataclasses import dataclass
from typing import Optional
import logging

@dataclass
class HallBayesConfig:
    """Configuración segura para HallBayes"""
    api_key: Optional[str] = None
    model: str = "gpt-4o-mini"
    temperature: float = 0.3
    abstention_threshold: float = 0.05
    max_cost_per_query: float = 0.05
    enable_caching: bool = True
    
@dataclass  
class IntegridAIConfig:
    """Configuración para IntegridAI DSP"""
    dsp_tau: float = 0.8
    cultural_factor: float = 1.2
    legal_mode: bool = True
    enable_audit: bool = True

@dataclass
class SecurityConfig:
    """Configuración de seguridad"""
    debug_mode: bool = False
    log_level: str = "INFO"
    enable_audit_trail: bool = True
    mask_api_keys: bool = True
    max_retries: int = 3

class ConfigManager:
    """Gestor seguro de configuración"""
    
    def __init__(self, env_file: str = ".env"):
        self.env_file = env_file
        self._load_env()
        
    def _load_env(self):
        """Carga variables de entorno de forma segura"""
        env_path = os.path.join(os.path.dirname(__file__), "..", self.env_file)
        
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value
    
    def get_hallbayes_config(self) -> HallBayesConfig:
        """Obtiene configuración HallBayes de forma segura"""
        
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            logging.warning("🔑 OPENAI_API_KEY no encontrada. Usando modo demo.")
            api_key = None
            
        return HallBayesConfig(
            api_key=api_key,
            model=os.getenv('HALLBAYES_MODEL', 'gpt-4o-mini'),
            temperature=float(os.getenv('HALLBAYES_TEMPERATURE', '0.3')),
            abstention_threshold=float(os.getenv('HALLBAYES_ABSTENTION_THRESHOLD', '0.05')),
            max_cost_per_query=float(os.getenv('HALLBAYES_MAX_COST_PER_QUERY', '0.05')),
            enable_caching=os.getenv('HALLBAYES_CACHING', 'true').lower() == 'true'
        )
    
    def get_integridai_config(self) -> IntegridAIConfig:
        """Obtiene configuración IntegridAI"""
        return IntegridAIConfig(
            dsp_tau=float(os.getenv('INTEGRIDAI_DSP_TAU', '0.8')),
            cultural_factor=float(os.getenv('INTEGRIDAI_CULTURAL_FACTOR', '1.2')),
            legal_mode=os.getenv('INTEGRIDAI_LEGAL_MODE', 'true').lower() == 'true',
            enable_audit=os.getenv('ENABLE_AUDIT_TRAIL', 'true').lower() == 'true'
        )
    
    def get_security_config(self) -> SecurityConfig:
        """Obtiene configuración de seguridad"""
        return SecurityConfig(
            debug_mode=os.getenv('DEBUG_MODE', 'false').lower() == 'true',
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            enable_audit_trail=os.getenv('ENABLE_AUDIT_TRAIL', 'true').lower() == 'true',
            mask_api_keys=os.getenv('MASK_API_KEYS', 'true').lower() == 'true',
            max_retries=int(os.getenv('MAX_RETRIES', '3'))
        )
    
    def validate_configuration(self) -> bool:
        """Valida que la configuración sea correcta"""
        config = self.get_hallbayes_config()
        
        if not config.api_key:
            print("⚠️  OpenAI API key no configurada - funcionará en modo demo")
            return False
            
        if config.api_key and not config.api_key.startswith(('sk-', 'sk-proj-')):
            print("❌ Formato de API key incorrecto")
            return False
            
        print("✅ Configuración validada correctamente")
        return True
    
    def mask_sensitive_data(self, data: str) -> str:
        """Enmascara datos sensibles para logs"""
        if not data or len(data) < 10:
            return "***"
        return f"{data[:7]}***{data[-4:]}"

# Instancia global del gestor de configuración
config_manager = ConfigManager()

def get_config():
    """Función helper para obtener configuración"""
    return {
        'hallbayes': config_manager.get_hallbayes_config(),
        'integridai': config_manager.get_integridai_config(), 
        'security': config_manager.get_security_config()
    }

if __name__ == "__main__":
    # Test de configuración
    print("🔧 Testing configuración...")
    config_manager.validate_configuration()
    
    configs = get_config()
    print(f"📊 HallBayes Model: {configs['hallbayes'].model}")
    print(f"📊 Temperature: {configs['hallbayes'].temperature}")
    print(f"🛡️ Abstention Threshold: {configs['hallbayes'].abstention_threshold}")
    
    if configs['hallbayes'].api_key:
        masked_key = config_manager.mask_sensitive_data(configs['hallbayes'].api_key)
        print(f"🔑 API Key: {masked_key}")
    else:
        print("🔑 API Key: No configurada (modo demo)")