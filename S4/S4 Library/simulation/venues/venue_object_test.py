from event_testing.tests_object import NumberTaggedObjectsOwnedFactory
from sims4.localization import TunableLocalizedString
from sims4.tuning.dynamic_enum import DynamicEnum
from sims4.tuning.tunable import TunableTuple, TunableRange, TunableList, TunableEnumEntry, Tunable
from sims4.tuning.tunable_base import ExportModes

class TunableVenueObjectTags(NumberTaggedObjectsOwnedFactory):

    def __init__(self, **kwargs):
        (super().__init__(locked_args={'desired_state': None}, **kwargs),)

class TunableVenueObject(TunableTuple):

    def __init__(self, **kwargs):
        super().__init__(object=TunableVenueObjectTags(description="\n                Specify object tag(s) that must be on this venue. Allows you to\n                group objects, i.e. weight bench, treadmill, and basketball\n                goals are tagged as\n                'exercise objects.'\n                ", export_modes=ExportModes.All), number=TunableRange(description='\n                Number of the tuned object that have to be on the venue. Ex\n                Barstools 4 means you have to have at least 4 barstools before\n                it can be this venue.\n                ', tunable_type=int, default=1, minimum=1, export_modes=ExportModes.All), object_display_name=TunableLocalizedString(description='\n                Name that will be displayed for the object(s)\n                ', allow_catalog_name=True, export_modes=ExportModes.All), **kwargs)

class VenueObjectTestTag(DynamicEnum):
    INVALID = 0

class TunableVenueObjectWithPair(TunableTuple):

    def __init__(self, **kwargs):
        super().__init__(object=TunableVenueObjectTags(description="\n                Specify object tag(s) that must be on this venue. Allows you to\n                group objects, i.e. weight bench, treadmill, and basketball\n                goals are tagged as\n                'exercise objects.'\n                ", export_modes=ExportModes.All), object_parent_pair_tests=TunableList(description="\n                Specify object tag(s) and/or parent attachment tags that\n                requires to be on this venue. Allows you to group objects, i.e.\n                weight bench, treadmill, and basketball goals are tagged as\n                'exercise objects.'\n                ", tunable=TunableTuple(object_tags=TunableVenueObjectTags(description='\n                        The objects (tag) that would count for the required items.\n                        ', export_modes=ExportModes.All), parent_tags=TunableVenueObjectTags(description='\n                        If set, the object tuned in object_tags would required\n                        to be slotted to the parent object tuned in\n                        parent_tags. \n                        \n                        E.g. in restaurant, a chair (with restaurant_chair tag)\n                        would need to slot to a table (with\n                        restaurant_table_tag) to count as a dining slot. But\n                        since bar will not has the restaurant_table_tag, so a\n                        high chair that slots to the bar will not count as\n                        dining spot.\n                        ', export_modes=ExportModes.All), count=TunableRange(description='\n                        How many required objects will be satisfied with this\n                        object(and/or with parent pair).\n                        \n                        E.g. a chair that slots to table will count as one\n                        dining spot, but booth slot to table will count as 2.\n                        ', tunable_type=int, default=1, minimum=1), required_object_test_tag=TunableEnumEntry(tunable_type=VenueObjectTestTag, default=VenueObjectTestTag.INVALID), export_class_name='VenueObjectParentPairTuple', export_modes=ExportModes.All)), number=TunableRange(description='\n                Number of the tuned object that have to be on the venue. Ex\n                Barstools 4 means you have to have at least 4 barstools before\n                it can be this venue.\n                ', tunable_type=int, default=1, minimum=1, export_modes=ExportModes.All), object_display_name=TunableLocalizedString(description='\n                Name that will be displayed for the object(s)\n                ', allow_catalog_name=True, export_modes=ExportModes.All), is_optional=Tunable(description='\n                If True, this object requirement will be optional to this venue.\n                \n                E.g. Waiter station and host station for restaurant should set\n                this entry to True.\n                ', tunable_type=bool, default=False, export_modes=ExportModes.All), is_pool_object=Tunable(description='\n                True if this venue requires a pool to satisfy eligibility\n                ', tunable_type=bool, default=False, export_modes=ExportModes.All), **kwargs)
