from collections import OrderedDict
import copy
from animation.animation_element import TunableAnimationOverrides
from objects.part import ObjectPart
from sims4.tuning.geometric import TunableVector2
from sims4.tuning.tunable import HasTunableSingletonFactory, AutoFactoryInit, TunableList, OptionalTunable, Tunable, TunableMapping
from sims4.tuning.tunable_base import TunableBase
import sims4.log
logger = sims4.log.Logger('Parts')

class _PartData(HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'part_definition': ObjectPart.TunableReference(description='\n            The part definition associated with this part instance.\n            \n            The part definition defines supported postures and interactions,\n            disallowed buffs and portal data.\n            ', pack_safe=True), 'adjacent_parts': TunableList(description='\n            The parts that are adjacent to this part. You must reference a part\n            that is tuned in this mapping.\n            \n            An empty list indicates that no part is adjacent to this part.\n            ', tunable=Tunable(tunable_type=str, default=None), unique_entries=True), 'overlapping_parts': TunableList(description='\n            The parts that are unusable when this part is in use. You must\n            reference a part that is tuned in this mapping.\n            ', tunable=Tunable(tunable_type=str, default=None), unique_entries=True), 'subroot_index': OptionalTunable(description='\n            If enabled, this part will have a subroot index associated with it.\n            This will affect the way Sims animate, i.e. they will animate\n            relative to the position of the part, not relative to the object.\n            ', tunable=Tunable(description='\n                The subroot suffix associated with this part.\n                ', tunable_type=int, default=0, needs_tuning=False), enabled_by_default=True), 'anim_overrides': TunableAnimationOverrides(description='\n            Animation overrides for this part.\n            '), 'is_mirrored': OptionalTunable(description='\n            Specify whether or not solo animations played on this part\n            should be mirrored or not.\n            ', tunable=Tunable(description='\n                If checked, mirroring is enabled. If unchecked,\n                mirroring is disabled.\n                ', tunable_type=bool, default=False)), 'forward_direction_for_picking': TunableVector2(description="\n            When you click on the object this part belongs to, this offset will\n            be applied to this part when determining which part is closest to\n            where you clicked.\n            \n            By default, the object's forward vector will be used. It should only\n            be necessary to tune this value if multiple parts overlap at the\n            same location (e.g. the single bed).\n            ", default=TunableVector2.DEFAULT_Z, x_axis_name='x', y_axis_name='z'), 'disable_sim_aop_forwarding': Tunable(description='\n            If checked, Sims using this specific part will never forward\n            AOPs.\n            ', tunable_type=bool, default=False), 'disable_child_aop_forwarding': Tunable(description='\n            If checked, objects parented to this specific part will\n            never forward AOPs.\n            ', tunable_type=bool, default=False)}

class TunablePartDataMapping(TunableMapping):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, key_type=Tunable(description='\n                A unique, arbitrary identifier for this part. Use this to define\n                adjacent and overlapping parts.\n                ', tunable_type=str, default=None), value_type=_PartData.TunableFactory(), **kwargs)

    @property
    def export_class(self):
        return 'TunableMapping'

    def load_etree_node(self, *args, source, **kwargs):
        value = super().load_etree_node(*args, source=source, **kwargs)
        value = OrderedDict(sorted(value.items()))
        index_map = {k: i for (i, k) in enumerate(value)}
        values = []
        for (k, v) in value.items():
            v = copy.copy(v)
            adjacent_parts = tuple(index_map[i] for i in v.adjacent_parts if i in index_map)
            setattr(v, 'adjacent_parts', adjacent_parts)
            overlapping_parts = tuple(index_map[i] for i in v.overlapping_parts if i in index_map)
            setattr(v, 'overlapping_parts', overlapping_parts)
            values.append(v)
        return tuple(values)

    def invoke_callback(self, instance_class, tunable_name, source, value):
        if not self._has_callback:
            return
        TunableBase.invoke_callback(self, instance_class, tunable_name, source, value)
        if value is not None:
            template = self._template.tunable_items['value']
            for tuned_value in value:
                template.invoke_callback(instance_class, tunable_name, source, tuned_value)

    def invoke_verify_tunable_callback(self, instance_class, tunable_name, source, value):
        if not self._has_verify_tunable_callback:
            return
        TunableBase.invoke_verify_tunable_callback(self, instance_class, tunable_name, source, value)
        if value is not None:
            template = self._template.tunable_items['value']
            for tuned_value in value:
                template.invoke_verify_tunable_callback(instance_class, tunable_name, source, tuned_value)