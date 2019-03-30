from sims4.tuning.tunable import TunableVariant, HasTunableSingletonFactory, AutoFactoryInit, TunableList, TunableTuple
from event_testing.tests import TunableTestSet

class TunableTestedVariant(TunableVariant):

    @staticmethod
    def _create_tested_selector(tunable_type, is_noncallable_type=False):

        class _TestedSelector(HasTunableSingletonFactory, AutoFactoryInit):
            FACTORY_TUNABLES = {'records': TunableList(tunable=TunableTuple(tests=TunableTestSet(), item=tunable_type))}

            def __call__(self, *args, resolver=None, **kwargs):
                for item_pair in self.records:
                    if item_pair.tests.run_tests(resolver):
                        if is_noncallable_type:
                            return item_pair.item
                        return item_pair.item(*args, resolver=resolver, **kwargs)

        return _TestedSelector.TunableFactory()

    @staticmethod
    def _create_noncallable_item_factory(tunable_type):

        class _NonCallableItem(HasTunableSingletonFactory, AutoFactoryInit):
            FACTORY_TUNABLES = {'item': tunable_type}

            def __call__(self, *args, **kwargs):
                return self.item

        return _NonCallableItem.TunableFactory()

    def __init__(self, tunable_type, is_noncallable_type=False, **kwargs):
        super().__init__(single=TunableTestedVariant._create_noncallable_item_factory(tunable_type) if is_noncallable_type else tunable_type, tested=TunableTestedVariant._create_tested_selector(tunable_type, is_noncallable_type=is_noncallable_type), default='single', **kwargs)