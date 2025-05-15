from netbox.api.viewsets import NetBoxModelViewSet

from .. import models, filtersets
from . import serializers

# ThreatSource ViewSets

class ThreatSourceViewSet(NetBoxModelViewSet):
    queryset = models.ThreatSource.objects.all()
    serializer_class = serializers.ThreatSourceSerializer
    filterset_class = filtersets.ThreatSourceFilterSet
    
# ThreatEvent ViewSets

class ThreatEventViewSet(NetBoxModelViewSet):
    queryset = models.ThreatEvent.objects.all()
    serializer_class = serializers.ThreatEventSerializer
    filterset_class = filtersets.ThreatEventFilterSet

# Vulnerability ViewSets

class VulnerabilityViewSet(NetBoxModelViewSet):
    queryset = models.Vulnerability.objects.all()
    serializer_class = serializers.VulnerabilitySerializer
    filterset_class = filtersets.VulnerabilityFilterSet
    
# VulnerabilityAssignment ViewSets

class VulnerabilityAssignmentViewSet(NetBoxModelViewSet):
    queryset = models.VulnerabilityAssignment.objects.all()
    serializer_class = serializers.VulnerabilityAssignmentSerializer
    filterset_class = filtersets.VulnerabilityAssignmentFilterSet

# Risk ViewSets

class RiskViewSet(NetBoxModelViewSet):
    queryset = models.Risk.objects.all()
    serializer_class = serializers.RiskSerializer
    filterset_class = filtersets.RiskFilterSet

# Control ViewSets

class ControlViewSet(NetBoxModelViewSet):
    queryset = models.Control.objects.all()
    serializer_class = serializers.ControlSerializer
    filterset_class = filtersets.ControlFilterSet