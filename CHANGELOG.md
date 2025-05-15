# Changelog

## Version 43.0.2 (2025-05-15)
* Corrigido modelo VulnerabilityAssignment (anteriormente com erro ortográfico)
* Corrigido campo impact em ThreatEvent (removido unique e adicionado choices)
* Renomeado campo vulnerability para vulnerabilities em ThreatEvent
* Adicionados verbose_names adequados para campos relacionados
* Removido max_length incorreto do campo cvssbaseScore em Vulnerability
* Adicionada migração para corrigir estrutura do banco de dados

## Version 43.0.1 (2025-05-14)
* Corrigida estrutura do pacote para instalação adequada
* Adicionados arquivos __init__.py faltantes
* Atualizado MANIFEST.in e setup.py

## Version 43.0.0 (2025-05-14)
* Added compatibility with NetBox 4.3.x
* Updated models to include ordering
* Replaced dcim.site with dcim.location for model references
* Updated template extensions to use models instead of model
* Fixed serializers to work with the latest NetBox API

## Version 41.0.2
* Added Netbox 4.1 Compatibility.

## 35.1.0 (18/08/2023)
* Add case sensitive name constrain to Vulnerability model
* Change the import path of get_plugin_config() to extras.plugins.utils [13368](https://github.com/netbox-community/netbox/commit/f5a1f83f9fa9d98c945d21eb0f7ccb8cd37fbf59)