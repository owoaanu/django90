# blog/api/metadata.py (create this module)
from rest_framework.metadata import SimpleMetadata

class CustomMetadata(SimpleMetadata):
    def determine_metadata(self, request, view):
        meta = super().determine_metadata(request, view)
        # Enrich with friendly labels the UI/tools can read
        meta["x-title"] = getattr(view, "meta_title", view.get_view_name())
        meta["x-description"] = getattr(view, "meta_description", view.get_view_description())
        return meta
        