from event_testing.tests import TunableTestSet
from interactions import ParticipantType
from interactions.utils.interaction_elements import XevtTriggeredElement
from objects.gardening.gardening_tuning import GardeningTuning
from objects.slot_strategy import SlotStrategyVariant
from sims4.tuning.tunable import HasTunableFactory, AutoFactoryInit, OptionalTunable, Tunable
from tunable_utils.tunable_object_generator import TunableObjectGeneratorVariant
from ui.ui_dialog_notification import TunableUiDialogNotificationSnippet
import build_buy
import services
import sims4.log
logger = sims4.log.Logger('SlotElements', default_owner='rmccord')

class SlotObjectsFromInventory(XevtTriggeredElement, HasTunableFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'description': '\n            Transfer particpant objects into the target object available slots\n            of the tuned slot type. \n            ', 'slot_strategy': SlotStrategyVariant(description='\n            The slot strategy we want to use to place objects from the transfer\n            source into slots on the target.\n            '), 'slot_failure_notification': OptionalTunable(description='\n            If enabled, we will show a notification to the player when this\n            element runs and no objects are successfully slotted.\n            ', tunable=TunableUiDialogNotificationSnippet(description='\n                Notification to show if we fail to slot any objects.\n                '))}

    def _do_behavior(self):
        slot_strategy = self.slot_strategy(self.interaction.get_resolver())
        if slot_strategy.slot_objects() or self.slot_failure_notification is not None:
            dialog = self.slot_failure_notification(self.interaction.sim, resolver=self.interaction.get_resolver())
            dialog.show_dialog()
        return True

class SlotItemTransfer(XevtTriggeredElement, HasTunableFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {'objects_to_transfer': TunableObjectGeneratorVariant(description="\n            The objects whose slots will be checked for objects to be gathered\n            into the Sim's inventory.\n            ", participant_default=ParticipantType.Object), 'object_tests': TunableTestSet(description='\n            Tests that will run on each object, and will harvest the object\n            only if all the tests pass.\n            \n            The object will be the PickedObject participant type, so we can\n            preserve the interaction resolver.\n            '), 'fallback_to_household_inventory': Tunable(description="\n            If enabled, and we fail to add the object to the Sim's inventory,\n            we will attempt to add it to the household inventory.\n            ", tunable_type=bool, default=False)}

    def _do_behavior(self):
        objects = self.objects_to_transfer.get_objects(self.interaction)
        if not objects:
            return False
        objects_to_transfer = []
        for obj in objects:
            for child_inst in obj.children:
                interaction_parameters = {'picked_item_ids': (child_inst.id,)}
                resolver = self.interaction.get_resolver(**interaction_parameters)
                if self.object_tests.run_tests(resolver):
                    objects_to_transfer.append(child_inst)
        stacked_objects = self._stack_objects_transfer(objects_to_transfer)
        sim = self.interaction.sim
        sim_inventory = sim.inventory_component
        for (obj, _) in stacked_objects:
            obj.update_ownership(sim)
            if sim_inventory.player_try_add_object(obj):
                if obj.live_drag_component is not None:
                    obj.live_drag_component.resolve_live_drag_household_permission()
                    if self.fallback_to_household_inventory:
                        build_buy.move_object_to_household_inventory(obj)
            elif self.fallback_to_household_inventory:
                build_buy.move_object_to_household_inventory(obj)

    def _stack_objects_transfer(self, objects_to_harvest):
        obj_count = {}
        unique_objects = []
        dupe_objects = []
        while objects_to_harvest:
            obj = objects_to_harvest.pop()
            quality_value = obj.get_state(GardeningTuning.QUALITY_STATE_VALUE) if obj.has_state(GardeningTuning.QUALITY_STATE_VALUE) else 0
            object_count_key = (obj.guid64, quality_value)
            curr_count = obj_count.get(object_count_key, 0)
            if curr_count == 0:
                unique_objects.append((obj, quality_value))
            else:
                dupe_objects.append(obj)
            curr_count = curr_count + 1
            obj_count[object_count_key] = curr_count
        for (obj, quality_value) in unique_objects:
            object_count_key = (obj.guid64, quality_value)
            curr_count = obj_count.get(object_count_key, 0)
            obj.set_stack_count(curr_count)
        services.get_reset_and_delete_service().trigger_batch_destroy(dupe_objects)
        return unique_objects