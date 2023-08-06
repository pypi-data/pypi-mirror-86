from django.apps import AppConfig


class EssentialsKitManagementV2AppConfig(AppConfig):
    name = "essentials_kit_management_v2"

    def ready(self):
        from essentials_kit_management_v2 import signals # pylint: disable=unused-variable
