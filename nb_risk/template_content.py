from netbox.plugins import PluginTemplateExtension
from netbox.plugins.utils import get_plugin_config
from django.conf import settings
from packaging import version

# Extract only the base version (e.g., '4.3.1' from '4.3.1-Docker-3.3.0')
raw_version = settings.VERSION
base_version_str = raw_version.split('-')[0]
NETBOX_CURRENT_VERSION = version.parse(base_version_str)


def create_button(model_name):
    class Button(PluginTemplateExtension):
        models = [model_name]

        def buttons(self):
            return self.render("nb_risk/vulnerability_assignment_button.html")

    return Button


supported_assets = get_plugin_config("nb_risk", "supported_assets")
additional_assets = get_plugin_config("nb_risk", "additional_assets")
supported_assets = supported_assets + additional_assets

template_extensions = []
for supported_asset in supported_assets:
    template_extensions.append(create_button(supported_asset))
