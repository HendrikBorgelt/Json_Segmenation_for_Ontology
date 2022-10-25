import types
import owlready2


def add_basic_props_to_emmo(emmo_int):
    with emmo_int:
        __hasSimulation__ = types.new_class('hasSimulation', (owlready2.ObjectProperty,))
        __hasSimulation__.prefLabel = [owlready2.locstr('hasSimulation', lang='en')]
        __isSimulationOf__ = types.new_class('isSimulationOf', (owlready2.ObjectProperty,))
        __isSimulationOf__.prefLabel = [owlready2.locstr('isSimulationOf', lang='en')]
        __hasSimulation__.inverse_property = __isSimulationOf__
        __hasIndividual__ = types.new_class('hasIndividual', (owlready2.ObjectProperty,))
        __hasIndividual__.prefLabel = [owlready2.locstr('hasIndividual', lang='en')]
        __isIndividualOf__ = types.new_class('isIndividualOf', (owlready2.ObjectProperty,))
        __hasIndividual__.inverse_property = __isIndividualOf__
        __hasDefinedIndividual__ = types.new_class('hasDefinedIndividual', (owlready2.ObjectProperty,))
        __hasDefinedIndividual__.prefLabel = [owlready2.locstr('hasDefinedIndividual', lang='en')]
        __isDefinedIndividualOf__ = types.new_class('isDefinedIndividualOf', (owlready2.ObjectProperty,))
        __isDefinedIndividualOf__.prefLabel = [owlready2.locstr('isDefinedIndividualOf', lang='en')]
        __hasDefinedIndividual__.inverse_property = __isDefinedIndividualOf__
        __hasSetting__ = types.new_class('hasSetting', (owlready2.ObjectProperty,))
        __hasSetting__.prefLabel = [owlready2.locstr('hasSetting', lang='en')]
        __hasOption__ = types.new_class('hasOption', (owlready2.DataProperty,))
        __hasOption__.prefLabel = [owlready2.locstr('hasOption', lang='en')]
    return emmo_int

