import os
import tarfile
import glob

import pandas as pd

from road_collisions_base import logger
from road_collisions_base.models.generic import GenericObjects
from road_collisions_base.models.raw_collision import RawCollision


class Collisions(GenericObjects):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('child_class', RawCollision)
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_file(filepath, year=None):
        data = None

        ext = os.path.splitext(filepath)[-1]
        if ext == '.tgz' or ext == '.gz':
            tar = tarfile.open(filepath, "r:gz")
            tar.extractall(path=os.path.dirname(filepath))
            tar.close()

            data = []
            for sub_file in glob.iglob(os.path.dirname(filepath) + '/**', recursive=True):
                ext = os.path.splitext(sub_file)[-1]
                if ext == '.csv':
                    csv_data = pd.read_csv(
                        sub_file.replace('.csv.tgz', '.csv')
                    ).to_dict(orient='records')

                    if year is None:
                        data.extend(csv_data)
                    else:
                        data.extend([d for d in csv_data if d['C_YEAR'] == year])

        else:
            raise Exception()

        collisions = Collisions()
        for collision_dict in data:
            obj = Collision.parse(
                collision_dict
            )

            # TODO: filter the object out here by whatever prop params
            # and save some mem

            collisions.append(obj)

        return collisions

    @staticmethod
    def from_dir(dirpath, region=None, year=None):
        collisions = Collisions()
        if region is None:
            search_dir = f'{dirpath}/**'
        else:
            search_dir = f'{dirpath}/{region}/**'

        for filename in glob.iglob(search_dir, recursive=True):
            if os.path.splitext(filename)[-1] not in {'.tgz', '.gz'}:
                continue
           
            collision = Collisions.from_file(
                filename,
                year=year
            )

            collisions.extend(
                collision
            )

        return collisions

    def filter(self, **kwargs):
        '''
        By whatever props that exist
        '''
        logger.debug('Filtering from %s' % (len(self)))

        filtered = [
            d for d in self if all(
                [
                    getattr(d, attr) == kwargs[attr] for attr in kwargs.keys()
                ]
            )
        ]

        return Collisions(
            data=filtered
        )

    @staticmethod
    def load_all(region=None, year=None):
        import road_collisions_canada
        return Collisions.from_dir(
            os.path.join(road_collisions_canada.__path__[0], 'resources'),
            region=region,
            year=year
        )


class Collision(RawCollision):

    __slots__ = [
        '_c_year',
        '_c_month',
        '_c_weekday',
        '_c_hour',
        '_c_severity',
        '_c_vehicles',
        '_c_configuration',
        '_c_road_configuration',
        '_c_weather',
        '_c_road_surface',
        '_c_road_alignment',
        '_c_traffic',
        '_v_id',
        '_v_type',
        '_v_year',
        '_p_id',
        '_p_sex',
        '_p_age',
        '_p_position',
        '_p_isev',
        '_p_safety_device',
        '_p_user',
        '_c_case'
    ]

    def __init__(self, **kwargs):

        # Can we split into vehicle etc? What is the key to join?

        self._c_year = kwargs['C_YEAR']
        self._c_mnth = kwargs['C_MNTH']
        self._c_wday = kwargs['C_WDAY']
        self._c_hour = kwargs['C_HOUR']
        self._c_sev = kwargs['C_SEV']
        self._c_vehs = kwargs['C_VEHS']
        self._c_conf = kwargs['C_CONF']
        self._c_rcfg = kwargs['C_RCFG']
        self._c_wthr = kwargs['C_WTHR']
        self._c_rsur = kwargs['C_RSUR']
        self._c_raln = kwargs['C_RALN']
        self._c_traf = kwargs['C_TRAF']
        self._c_case = kwargs['C_CASE']
        self._v_id = kwargs['V_ID']
        self._v_type = kwargs['V_TYPE']
        self._v_year = kwargs['V_YEAR']
        self._p_id = kwargs['P_ID']
        self._p_sex = kwargs['P_SEX']
        self._p_age = kwargs['P_AGE']
        self._p_psn = kwargs['P_PSN']
        self._p_isev = kwargs['P_ISEV']
        self._p_safe = kwargs['P_SAFE']
        self._p_user = kwargs['P_USER']

    @staticmethod
    def parse(data):
        if isinstance(data, Collision):
            return data

        return Collision(
            **data
        )

    def serialize(self):
        return {
            'c_year': self.c_year,
            'c_month': self.c_month,
            'c_weekday': self.c_weekday,
            'c_hour': self.c_hour,
            'c_severity': self.c_severity,
            'c_vehicles': self.c_vehicles,
            'c_configuration': self.c_configuration,
            'c_road_configuration': self.c_road_configuration,
            'c_weather': self.c_weather,
            'c_road_surface': self.c_road_surface,
            'c_road_alignment': self.c_road_alignment,
            'c_traffic': self.c_traffic,
            'v_id': self.v_id,
            'v_type': self.v_type,
            'v_year': self.v_year,
            'p_id': self.p_id,
            'p_sex': self.p_sex,
            'p_age': self.p_age,
            'p_position': self.p_position,
            'p_isev': self.p_isev,
            'p_safety_device': self.p_safety_device,
            'p_user': self.p_user,
            'c_case': self.c_case
        }

    @property
    def c_year(self):
        return self._c_year

    @property
    def c_month(self):
        try:
            return [None, 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'][int(self._c_mnth)]
        except ValueError:
            # warn
            return None

    @property
    def c_weekday(self):
        try:
            return [None, 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'][int(self._c_wday)]
        except ValueError:
            # warn
            return None

    @property
    def c_hour(self):
        return self._c_hour

    @property
    def c_severity(self):
        return {
            1: 'no_injury',
            2: 'injury',
            3: 'fatality'
        }[self._c_sev]

    @property
    def c_vehicles(self):
        return self._c_vehs

    @property
    def c_configuration(self):
        try:
            return {
                1: 'hit_moving_object',
                2: 'hit_stationary_object',
                3: 'ran_off_left_shoulder',
                4: 'ran_off_right_shoulder',
                5: 'rollover_on_roadway',
                6: 'other_single_vehicle_collision',
                21: 'rear_end_collision',
                22: 'side_swipe',
                23: '1_vehicle_passing_to_the_left_of_the_other/left_turn_conflict',
                24: '1_vehicle_passing_to_the_right_of_the_other/or_right_turn_conflict',
                25: 'other_2_vehicle-same_direction_of_travel',
                31: 'head_on_collisions',
                32: 'approaching_side_swipe',
                33: 'left_turn_across_opposing_traffic',
                34: 'right_turn_oncluding_turning_conflicts',
                35: 'right_angle_collision',
                36: 'any_other_two_vehicle',
                41: 'hit_a_parked_motor_vehicle'
            }[int(self._c_conf)]
        except ValueError:
            return self._c_conf

    @property
    def c_road_configuration(self):
        try:
            return [
                None,
                'mid_block',
                'at_an_intersection',
                'intersection_with_parking_lot_entrance/exit',
                'railroad_crossing',
                'bridge',
                'tunnel',
                'passing_or_climbing_lane',
                'ramp',
                'traffic_circle',
                'highway_express_lane',
                'highway_collector_lane',
                'highway_transfer_lane'
            ][int(self._c_rcfg)]
        except ValueError:
            return None

    @property
    def c_weather(self):
        '''
        '''
        try:
            return [
                None,
                'clear_and_sunny',
                'overcast',
                'raining',
                'snowing',
                'freezing_rain_hail',
                'fog_smog_mist',
                'strong_wind'
            ][int(self._c_wthr)]
        except ValueError:
            return None

    @property
    def c_road_surface(self):
        try:
            return [
                None,
                'dry_normal',
                'wet',
                'snow',
                'slush_wet_snow',
                'icy',
                'sand_gravel_dirt',
                'muddy',
                'oil',
                'flooded'
            ][int(self._c_rsur)]
        except ValueError:
            return None

    @property
    def c_road_alignment(self):
        try:
            return {
                1: 'level_straight',
                2: 'gradient_straight',
                3: 'level_curved',
                4: 'gradient_curved',
                5: 'top_hill',
                6: 'bottom_hill',
            }[int(self._c_raln)]
        except ValueError:
            return None

    @property
    def c_traffic(self):
        try:
            return [
                None,
                'traffic_signals_fully_operational',
                'traffic_signals_in_flashing_mode',
                'stop_sign',
                'yield_sign',
                'warning_sign',
                'pedestrian_crosswalk',
                'police_officer',
                'school_guard',
                'school_crossing',
                'reduced_speed_zone',
                'no_passing_zone_sign',
                'markings_on_the_road',
                'school_bus_stopped_signal_lights_flashing',
                'railway_crossing_with_signals_and_gates',
                'railway_crossing_with_signs_only',
                'control_device_not_specified',
                'no_control_present'
            ][int(self._c_traf)]
        except (ValueError, IndexError):
            return None

    @property
    def v_id(self):  # what is this?
        return self._v_id

    @property
    def v_type(self):
        try:
            return {
                1: 'light_duty',
                5: 'cargo_less_than_4.5_t',
                6: 'truck_less_than_4.5_t',
                7: 'truck_greater_than_4.5_t',
                8: 'road_tractor',
                9: 'school_bus',
                10: 'small_school_bus',
                11: 'urban_bus',
                14: 'motorcycle',
                16: 'off_road',
                17: 'bicycle',
                18: 'motorhome',
                19: 'farm_equipment',
                20: 'construction',
                21: 'fire_engine',
                22: 'snowmobile',
                23: 'street_car',
            }[int(self._v_type)]
        except ValueError:
            return {
                'N': 'not_vehicle',
                'NN': 'not_vehicle',
                'Q': 'other',
                'QQ': 'other',
                'U': 'unknown',
                'UU': 'unknown',
            }[self._v_type]

    @property
    def v_year(self):
        return self._v_year

    @property
    def p_id(self):
        return self._p_id

    @property
    def p_sex(self):
        return self._p_sex

    @property
    def p_age(self):
        return self._p_age

    @property
    def p_position(self):
        try:
            return {
                11: 'driver',
                12: 'front_row_center',
                13: 'front_row_right_outboard',
                21: 'second_row_left_outboard',
                22: 'second_row_center',
                23: 'second_row_right_outboard',
                31: 'third_row_left_outboard',
                32: 'third_row_center',
                33: 'third_row_right_outboard',
                96: 'unknown_occupant',
                97: 'sitting_on_someones_lap',
                98: 'outside_passenger_compartment',
                99: 'pedestrian'
            }[int(self._p_psn)]
        except ValueError:
            # warn
            return None

    @property
    def p_isev(self):  # what is this?
        return self._p_isev

    @property
    def p_safety_device(self):
        try:
            return {
                1: 'no_safety_device_used',
                2: 'safety_device_used',
                9: 'helmet',
                10: 'reflective_clothing',
                11: 'helmet_and_reflective_clothing',
                12: 'other_safety_device_used',
                13: 'no_safety_device_equipped'
            }[int(self._p_safe)]
        except ValueError:
            # warn
            return None

    @property
    def p_user(self):  # what is this?
        return self._p_user

    @property
    def c_case(self):  # what is this?
        return self._c_case
