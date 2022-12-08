# encoding: utf-8

from APIs.TalpiotAPIs.AssessmentAPI.Database.api.docx_for_docm.api import Document  # noqa

__version__ = '0.8.1'


# register custom Part classes with opc package reader

from APIs.TalpiotAPIs.AssessmentAPI.Database.api.docx_for_docm.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.docx_for_docm.opc.part import PartFactory
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.docx_for_docm.opc.parts.coreprops import CorePropertiesPart

from APIs.TalpiotAPIs.AssessmentAPI.Database.api.docx_for_docm.parts.document import DocumentPart
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.docx_for_docm.parts.image import ImagePart
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.docx_for_docm.parts.numbering import NumberingPart
from APIs.TalpiotAPIs.AssessmentAPI.Database.api.docx_for_docm.parts.styles import StylesPart


def part_class_selector(content_type, reltype):
    if reltype == RT.IMAGE:
        return ImagePart
    return None


PartFactory.part_class_selector = part_class_selector
PartFactory.part_type_for[CT.OPC_CORE_PROPERTIES] = CorePropertiesPart
PartFactory.part_type_for[CT.WML_DOCUMENT_MAIN] = DocumentPart
PartFactory.part_type_for[CT.WML_NUMBERING] = NumberingPart
PartFactory.part_type_for[CT.WML_STYLES] = StylesPart
PartFactory.part_type_for[CT.WML_DOCUMENT_MACRO_ENABLED_MAIN] = DocumentPart

del (
    CT, CorePropertiesPart, DocumentPart, NumberingPart, PartFactory,
    StylesPart, part_class_selector
)
