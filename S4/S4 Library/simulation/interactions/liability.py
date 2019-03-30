from _weakrefset import WeakSet

class Liability:

    def release(self):
        pass

    def merge(self, interaction, key, new_liability):
        return new_liability

    def should_transfer(self, continuation):
        return True

    def transfer(self, interaction):
        pass

    def on_reset(self):
        self.release()

    def on_add(self, interaction):
        pass

    def on_run(self):
        pass

    def gsi_text(self):
        return type(self).__name__

    @classmethod
    def on_affordance_loaded_callback(cls, affordance, liability_tuning):
        pass

class ReplaceableLiability(Liability):

    def merge(self, interaction, key, new_liability):
        interaction.remove_liability(key)
        return new_liability

class SharedLiability(Liability):

    def __init__(self, *args, source_liability=None, **kwargs):
        super().__init__(**kwargs)
        self._released = False
        if source_liability is None:
            self._shared_liability_refs = WeakSet()
        else:
            self._shared_liability_refs = source_liability._shared_liability_refs
        self._shared_liability_refs.add(self)

    def shared_release(self):
        raise NotImplementedError('SharedLiability: {} trying to release with no shared_release implementation'.format(self))

    def release(self, *args, **kwargs):
        self._released = True
        if all(cur_liability._released for cur_liability in self._shared_liability_refs):
            self.shared_release(*args, **kwargs)

    def create_new_liability(self, interaction, *args, **kwargs):
        return self.__class__(*args, source_liability=self, **kwargs)