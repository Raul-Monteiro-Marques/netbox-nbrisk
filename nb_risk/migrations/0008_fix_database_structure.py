# Generated manually on 2025-05-15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nb_risk', '0007_remove_vulnerability_unique_vuln_name_and_more'),
    ]

    operations = [
        # Remover unique constraint do campo impact de ThreatEvent
        migrations.AlterField(
            model_name='threatevent',
            name='impact',
            field=models.CharField(
                choices=[
                    ('Very High', 'Very High'),
                    ('High', 'High'),
                    ('Moderate', 'Moderate'),
                    ('Low', 'Low'),
                    ('Very Low', 'Very Low'),
                ],
                default='Very High',
                max_length=100,
                verbose_name='Impact'
            ),
        ),
        # Renomear campo vulnerability para vulnerabilities em ThreatEvent
        migrations.RenameField(
            model_name='threatevent',
            old_name='vulnerability',
            new_name='vulnerabilities',
        ),
        # Adicionar verbose_name para o campo vulnerabilities em ThreatEvent
        migrations.AlterField(
            model_name='threatevent',
            name='vulnerabilities',
            field=models.ManyToManyField(
                blank=True,
                related_name='threat_events',
                to='nb_risk.vulnerabilityassignment',
                verbose_name='Vulnerabilities'
            ),
        ),
        # Adicionar verbose_name para o campo risk em Control
        migrations.AlterField(
            model_name='control',
            name='risk',
            field=models.ManyToManyField(
                blank=True,
                related_name='controls',
                to='nb_risk.risk',
                verbose_name='Risks'
            ),
        ),
        # Remover max_length do campo cvssbaseScore em Vulnerability
        migrations.AlterField(
            model_name='vulnerability',
            name='cvssbaseScore',
            field=models.FloatField(blank=True, null=True, verbose_name='Base Score'),
        ),
    ] 