from situations.complex.yoga_class import YogaClassScheduleMixin
from venues.scheduling_zone_director import SchedulingZoneDirector
from venues.visitor_situation_on_arrival_zone_director_mixin import VisitorSituationOnArrivalZoneDirectorMixin

class GymZoneDirector(YogaClassScheduleMixin, VisitorSituationOnArrivalZoneDirectorMixin, SchedulingZoneDirector):
    pass