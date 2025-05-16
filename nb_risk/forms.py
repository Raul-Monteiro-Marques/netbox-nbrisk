from django import forms
from django.contrib.contenttypes.models import ContentType

from netbox.forms import (
    NetBoxModelForm,
    NetBoxModelFilterSetForm,
    NetBoxModelBulkEditForm,
    NetBoxModelImportForm,
)
from ipam.models import IPAddress
from dcim.models import Device, DeviceType # Adicionado Device para o queryset de exemplo
from utilities.forms.fields import (
    DynamicModelMultipleChoiceField,
    SlugField,
    DynamicModelChoiceField,
    CSVModelMultipleChoiceField,
    CSVModelChoiceField,
    CSVContentTypeField,
    ContentTypeChoiceField, # Importação necessária
)
from utilities.forms.rendering import FieldSet
# from utilities.forms.widgets import ContentTypeSelect # ContentTypeChoiceField geralmente usa um widget padrão adequado

from . import models, choices

# ThreatSource Forms


class ThreatSourceForm(NetBoxModelForm):
    class Meta:
        model = models.ThreatSource
        fields = [
            "name",
            "threat_type",
            "capability",
            "intent",
            "targeting",
            "description",
            "notes",
            "tags", # Adicionar tags
        ]


class ThreatSourceFilterForm(NetBoxModelFilterSetForm):
    model = models.ThreatSource
    # Adicionar tag ao filter form se desejar filtrar por tags
    # tag = TagFilterField(model)

    class Meta: # Adicionar Meta ao FilterForm se não existir ou estiver incompleto
        fields = ["name", "threat_type", "capability", "intent", "targeting", "tags"]


class ThreatSourceImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.ThreatSource
        fields = [
            "name",
            "threat_type",
            "capability",
            "intent",
            "targeting",
            "description",
            "notes",
            # Adicionar tags se for importar
        ]

class ThreatSourceBulkEditForm(NetBoxModelBulkEditForm):
    model = models.ThreatSource

    # Se 'comments' não for um campo do modelo ThreatSource, remova-o ou defina-o corretamente.
    # Por padrão, NetBoxModelBulkEditForm lida com 'tags'.
    # Se 'description' e 'notes' são os campos que você quer editar em massa:
    description = forms.CharField(required=False)
    notes = forms.Textarea(
        attrs={'class': 'font-monospace'},
        required=False
    )
    # Adicionar outros campos do modelo ThreatSource que você quer que sejam editáveis em massa

    class Meta:
        nullable_fields = ("intent", "targeting", "description", "notes")


# ThreatEvent Forms


class ThreatEventForm(NetBoxModelForm):

    vulnerabilities = DynamicModelMultipleChoiceField(
        queryset=models.VulnerabilityAssignment.objects.all(),
        required=False,
    )
    # Adicionar o campo de seleção para ThreatSource se não estiver sendo pego automaticamente
    threat_source = DynamicModelChoiceField(
        queryset=models.ThreatSource.objects.all(),
        required=False # Baseado no seu models.py (blank=True, null=True)
    )

    class Meta:
        model = models.ThreatEvent
        fields = [
            "name",
            "threat_source",
            "description",
            "notes",
            "relevance",
            "likelihood",
            "impact",
            "vulnerabilities",
            "tags", # Adicionar tags
        ]


class ThreatEventFilterForm(NetBoxModelFilterSetForm):
    model = models.ThreatEvent
    # Adicionar os campos de filtro corretos
    threat_source = DynamicModelChoiceField(
        queryset=models.ThreatSource.objects.all(),
        required=False
    )
    vulnerabilities = DynamicModelMultipleChoiceField(
        queryset=models.VulnerabilityAssignment.objects.all(),
        required=False
    )
    # tag = TagFilterField(model)

    class Meta:
        fields = [
            "name",
            "threat_source",
            "relevance",
            "likelihood",
            "impact",
            "vulnerabilities", # Este é um ManyToMany, filtrar por ele pode ser complexo
            "tags",
        ]


# Vulnerability Forms


class VulnerabilityForm(NetBoxModelForm):

    fieldsets = (
        FieldSet("name", "cve", "description", "notes", "tags", name="Vulnerability"), # Adicionar tags ao fieldset
        FieldSet("cvssaccessVector", "cvssaccessComplexity", "cvssauthentication", "cvssconfidentialityImpact", "cvssintegrityImpact", "cvssavailabilityImpact", "cvssbaseScore", name="CVSSv2 Score"),
      )
      
    class Meta:
        model = models.Vulnerability
        fields = [
            "name",
            "cve",
            "description",
            "notes",
            "cvssaccessVector",
            "cvssaccessComplexity",
            "cvssauthentication",
            "cvssconfidentialityImpact",
            "cvssintegrityImpact",
            "cvssavailabilityImpact",
            "cvssbaseScore",
            "tags", # Adicionar tags
        ]


class VulnerabilityFilterForm(NetBoxModelFilterSetForm):
    model = models.Vulnerability
    # tag = TagFilterField(model)
    class Meta:
        fields = ["name", "cve", "tags"]


class VulnerabilitySearchFilterForm(NetBoxModelFilterSetForm): # Herdar de NetBoxModelFilterSetForm
    
    model = models.Vulnerability # Definir o modelo

    # Fieldsets são mais para forms de edição/criação, não tanto para filtros, mas podem ser usados para agrupar.
    # fieldsets = (
    #     FieldSet("cve", "keyword", name="CVE"),
    #     FieldSet("cpe", "device_type", "version", "part", name="CPE"),
    # )    

    cpe = forms.CharField(label="CPE Name", required=False)
    cve = forms.CharField(label="CVE", required=False)
    keyword = forms.CharField(label="Keyword", required=False)
    device_type = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
    )
    version = forms.CharField(required=False)
    part = forms.ChoiceField(
        choices=choices.CVE_PART_CHOICES, # Certifique-se que choices.CVE_PART_CHOICES está definido
        required=False,
    )
    # Adicionar Meta para definir os campos que o filtro usará
    class Meta:
        fields = ['cve', 'keyword', 'cpe', 'device_type', 'version', 'part']


class VulnerabilityImportForm(NetBoxModelImportForm):
    class Meta:
        model = models.Vulnerability
        fields = [
            "name",
            "cve",
            "description",
            "notes",
            "cvssaccessVector",
            "cvssaccessComplexity",
            "cvssauthentication",
            "cvssconfidentialityImpact",
            "cvssintegrityImpact",
            "cvssavailabilityImpact",
            "cvssbaseScore",
        ]

# VulnerabilityAssignment Forms

class VulnerabilityAssignmentForm(NetBoxModelForm): # MODIFICADO: Herdar de NetBoxModelForm
    
    asset_content_type = ContentTypeChoiceField(
        queryset=ContentType.objects.all(), # Você pode querer filtrar isso depois com base em 'additional_assets'
        label='Asset Type',
        # O widget padrão para ContentTypeChoiceField em NetBoxModelForm geralmente é adequado
    )

    # O DynamicModelChoiceField para asset_id precisa de um queryset.
    # O NetBox usa JavaScript para atualizar o queryset deste campo com base na seleção de asset_content_type.
    # Para que isso funcione, o widget do asset_id (geralmente APISelect)
    # precisa de parâmetros para a chamada AJAX (ex: query_params={'content_type_id': '$asset_content_type'}).
    # Vamos começar com um queryset genérico e um campo simples; pode precisar de ajustes.
    asset_id = DynamicModelChoiceField( # Usar DynamicModelChoiceField
        queryset=Device.objects.all(), # Exemplo inicial, o ideal é ser dinâmico
        label='Asset',
        # Se você estiver usando um widget como APISelect, você adicionaria:
        # widget=forms.Select(attrs={'data-query-param-content_type': 'asset_content_type_id'})
        # Ou similar, dependendo de como o JS do NetBox espera.
        # Por enquanto, vamos manter simples para ver se o botão aparece e o formulário básico renderiza.
    )

    vulnerability = DynamicModelChoiceField(
        queryset=models.Vulnerability.objects.all(),
        required=True,
    )
    
    # tags = TagField(required=False) # Se for usar tags do NetBox

    class Meta:
        model = models.VulnerabilityAssignment
        fields = [
            'asset_content_type', 
            'asset_id', 
            'vulnerability',
            'tags', # Adicionar 'tags' se for usar
        ]
        # Removidos os widgets HiddenInput


class VulnerabilityAssignmentFilterForm(NetBoxModelFilterSetForm):
    model = models.VulnerabilityAssignment
    
    asset_content_type = ContentTypeChoiceField(
        queryset=ContentType.objects.all(), # Filtrar conforme necessário
        required=False,
        label='Asset Type'
    )
    # Para asset_id no filtro, um campo de texto para o ID pode ser mais simples
    # ou um DynamicModelChoiceField se você tiver a lógica JS para populá-lo.
    # asset_id = forms.IntegerField(required=False, label='Asset ID')

    vulnerability = DynamicModelChoiceField(
        queryset=models.Vulnerability.objects.all(),
        required=False,
    )
    # tag = TagFilterField(model)

    class Meta: 
        fields = ['asset_content_type', 'vulnerability', 'tags'] # Adicionar 'tags' e outros campos de filtro


class VulnerabilityAssignmentImportForm(NetBoxModelImportForm):
    vulnerability = CSVModelChoiceField(
        label="Vulnerability",
        queryset=models.Vulnerability.objects.all(),
        required=True,
        to_field_name="name",
        error_messages={
            "invalid_choice": "Vulnerability name not found",
        }
    )

    asset_object_type = CSVContentTypeField(
        queryset=ContentType.objects.all(), # Filtrar se necessário
        help_text= "Assigned object types",
        required=False, # Mude para True se sempre for necessário um asset
    )
    
    # O asset_id precisaria ser validado em conjunto com asset_object_type no clean.
    # O CSVModelChoiceField não é ideal para asset_id diretamente sem saber o tipo.
    # A lógica no 'clean' já tenta lidar com isso via ip_address.

    ip_address = CSVModelChoiceField(
        label="IP Address (alternativa para encontrar o asset)",
        queryset= IPAddress.objects.all(),
        required=False,
        to_field_name='address',
        help_text="Se fornecido, o asset será inferido a partir do objeto ao qual este IP está atribuído.",
        error_messages={
            "invalid_choice": "IPAddress not found",
        }
    )

    # Removido asset_id do fields para o import se ele é inferido ou não usado diretamente.
    # Se você tiver colunas 'asset_object_type' (como string 'app_label.model') e 'asset_name_or_pk',
    # você precisaria de lógica customizada no 'clean' para buscar o asset_id.

    def clean(self):
        cleaned_data = super().clean()
        asset_type_from_field = cleaned_data.get("asset_object_type")
        # asset_id_from_field = cleaned_data.get("asset_id") # Se você tivesse um campo asset_id direto
        ip_address = cleaned_data.get("ip_address")
        vuln = cleaned_data.get("vulnerability")

        # Lógica para determinar o asset final (asset_type, asset_id)
        final_asset_type = None
        final_asset_id = None

        if ip_address:
            if not ip_address.assigned_object:
                raise forms.ValidationError(
                    f"IP Address ({ip_address}) is not assigned to any object"
                )
            # Tenta pegar o objeto pai (Device, VM) da Interface/VMInterface
            assigned_parent = getattr(ip_address.assigned_object, 'parent_object', None) # NetBox 3.7+
            if not assigned_parent and hasattr(ip_address.assigned_object, '_parent_object'): # Older NetBox
                 assigned_parent = getattr(ip_address.assigned_object, '_parent_object', None)
            
            target_object = assigned_parent if assigned_parent else ip_address.assigned_object

            final_asset_type = ContentType.objects.get_for_model(target_object)
            final_asset_id = target_object.id
            
            # Se asset_object_type também foi fornecido e difere do inferido pelo IP, pode ser um erro
            if asset_type_from_field and asset_type_from_field != final_asset_type:
                raise forms.ValidationError(
                    "Asset Type fornecido não corresponde ao Asset Type inferido do IP Address."
                )
        elif asset_type_from_field:
            # Se asset_object_type foi fornecido, você precisaria de uma forma de obter o asset_id
            # (ex: uma coluna 'asset_name' ou 'asset_pk' no CSV e buscá-lo aqui)
            # Por enquanto, esta lógica está incompleta sem um campo para identificar o asset.
            # raise forms.ValidationError("Se Asset Type é fornecido, uma forma de identificar o Asset ID também é necessária.")
            # Para este exemplo, vamos assumir que se asset_object_type é dado, asset_id também deveria ser
            # (o que não está no seu Meta fields para importação direta).
            # Esta parte precisaria de refinamento baseado no seu formato CSV.
            # Por ora, se asset_object_type é fornecido, esperamos que o asset_id seja preenchido por outra lógica
            # ou que o import não funcione corretamente sem o IP.
            pass # Placeholder para lógica de asset_id se não usar IP

        if final_asset_type and final_asset_id and vuln:
            if models.VulnerabilityAssignment.objects.filter(
                asset_object_type=final_asset_type, 
                asset_id=final_asset_id, 
                vulnerability=vuln
            ).exists():
                raise forms.ValidationError(
                    f"Vulnerability {vuln} is already assigned to asset {final_asset_type.model} ID {final_asset_id}"
                )
        
        # Atualizar cleaned_data com o asset_object_type e asset_id inferidos/validados
        if final_asset_type:
            cleaned_data['asset_object_type'] = final_asset_type
        if final_asset_id:
            cleaned_data['asset_id'] = final_asset_id
            
        if not cleaned_data.get('asset_id') and not ip_address : # Se nenhum asset foi identificado
             raise forms.ValidationError("Um Asset (via IP Address ou diretamente) deve ser especificado.")


        return cleaned_data
    
    class Meta:
        model = models.VulnerabilityAssignment
        fields = [ # Campos que o usuário fornecerá no CSV
            "vulnerability",
            "ip_address", # Principal forma de identificar o asset neste form
            "asset_object_type", # Opcional se ip_address for usado, mas pode ajudar a validar
            # "asset_id", # Removido daqui pois é inferido ou requer lógica mais complexa
            "tags",
        ]


# Risk Forms

class RiskForm(NetBoxModelForm):
    threat_event = DynamicModelChoiceField(
        queryset=models.ThreatEvent.objects.all()
    )
    class Meta:
        model = models.Risk
        fields = [
            "name",
            "threat_event",
            "description",
            "notes",
            "likelihood",
            "impact",
            "tags", # Adicionar tags
        ]


class RiskFilterForm(NetBoxModelFilterSetForm):
    model = models.Risk
    threat_event = DynamicModelChoiceField(
        queryset=models.ThreatEvent.objects.all(),
        required=False
    )
    # tag = TagFilterField(model)
    class Meta:
        fields = ["name", "threat_event", "description", "impact", "likelihood", "tags"]

# Control Forms

class ControlForm(NetBoxModelForm):
    risk = DynamicModelMultipleChoiceField(
        queryset=models.Risk.objects.all(),
        required=False
    )
    class Meta:
        model = models.Control
        fields = [
            "name",
            "description",
            "notes",
            "category",
            "risk",
            "tags", # Adicionar tags
        ]

class ControlFilterForm(NetBoxModelFilterSetForm):
    model = models.Control
    risk = DynamicModelMultipleChoiceField(
        queryset=models.Risk.objects.all(),
        required=False
    )
    # tag = TagFilterField(model)
    class Meta:
        fields = [
            "name",
            "description",
            "notes",
            "category",
            "risk",
            "tags",
        ]
