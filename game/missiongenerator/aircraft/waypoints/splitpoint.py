from dcs.point import MovingPoint
from dcs.task import OptECMUsing, OptFormation, RunScript

from game.utils import mach, Distance
from .pydcswaypointbuilder import PydcsWaypointBuilder


class SplitPointBuilder(PydcsWaypointBuilder):
    def add_tasks(self, waypoint: MovingPoint) -> None:

        if not self.flight.flight_type.is_air_to_air:
            # Capture any non A/A type to avoid issues with SPJs that use the primary radar such as the F/A-18C.
            # You can bully them with STT to not be able to fire radar guided missiles at you,
            # so best choice is to not let them perform jamming for now.

            # Let the AI use ECM to defend themselves.
            ecm_option = OptECMUsing(value=OptECMUsing.Values.UseIfOnlyLockByRadar)
            waypoint.tasks.append(ecm_option)

        waypoint.tasks.append(OptFormation.finger_four_close())
        waypoint.speed_locked = True
        waypoint.speed = self.flight.coalition.doctrine.rtb_speed.meters_per_second
        waypoint.ETA_locked = False
        if self.flight is self.package.primary_flight:
            script = RunScript(
                f'trigger.action.setUserFlag("split-{id(self.package)}", true)'
            )
            waypoint.tasks.append(script)
