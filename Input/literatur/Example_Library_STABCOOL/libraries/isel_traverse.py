### Author: f_scheiber
### For this class you need a serial connector, i.e. RS-232.
### Connect appropriate adapters and install corresponding drivers before usage.
### To use Prolific USB to serial adapter, first install the corresponding drivers from
### SLA:\09_LABOR\MESSTECHNIK - Unterlagen\GEITMANN_GOLDAMMER\SICONN USB_Basic\USB Seriell Adapter (blau)\PL2303_Prolific_DriverInstaller_v110.exe


import time
import serial
import numpy as np

test = False

error_codes = {
        # b'0': 'OK',
        b'1': 'Fehler in übergener Zahl\n-Die Steuerung hat eine Zahlenangabe empfangen, die nicht korrekt interpretiert werden konnte.\n-Der übergebene Zahlenwert ist außerhalb des zulässigen Bereichs oder der übergebene Zahlenwert enthält unzulässige Zeichen.',
        b'2': 'Endschalterfehler',
        b'3': 'Unzulässige Achsangabe',
        b'4': 'Keine Achsen definiert',
        b'5': 'Syntax-Fehler',
        b'6': 'Speicherende',
        b'7': 'Unzulässige Parameterzahl',
        b'8': 'Zu speichernder Befehl nicht korrekt',
        b'A': 'Impulsfehler',
        b'B': 'Tell-Fehler',
        b'C': '(CR) erwartet',
        b'D': 'Unzulässige Geschwindigkeit',
        b'E': 'Schleifenfehler',
        b'F': 'BenutzerStopp',
    }

def _error_check(error_code) -> str | None:
    return error_codes.get(bytes(error_code))

def hexb2int(bytestring):
    b = int(bytestring, 16)
    if b > int('F00000', 16):
        b -= int('1000000', 16)
    return b

class Isel_Axis:
    """
        Known Axes:
        - Isel LES 4 (thin with motor on the side): 234 101 0129
            - steigung [mm/rev] = 2.5
            - steps_per_rev [stp/rev] = 400 (200 + Halbschritt)
            - max_pos [mm] = 1220 (1290 - 70 (Schlittenlänge))
            - max_drehzahl [rev/min] = 3000 (long) / 4000 (short)
            - max_speed [mm/s] = 125 (long) / 167 (short)
            - position accuracy [mm]: +-0.02
        - Isel LES 5 (thick with motor at the end): 234 411 0079
            - steigung [mm/rev] = 2.5
            - steps_per_rev [stp/rev] = 400 (200 + Halbschritt)
            - max_pos [mm] = 590 (790 - 200 (Schlittenlänge))
            - max_drehzahl [rev/min] = 3000 (long) / 4000 (short)
            - max_speed [mm/s] = 125 (long) / 167 (short)
            - position accuracy [mm]: +-0.02

    """
    def __init__(self, name:str, steps_per_rev:int, steigung:float,
                 min_pos:float, max_pos:float,
                 max_speed:float = 100.):
        #axis direction / name
        self.name = name

        # physical axis properties --> dist [stp] = factor() [stp / mm] * dist [mm]
        self.steps_per_rev = steps_per_rev # [stp / rev]
        self.steigung = steigung # [mm / rev]

        # movement limits
        self.soft_limits = [min_pos, max_pos]
        self.max_speed = max_speed

        # current parameters in mm and s
        self.position = None
        self.speed = 10.
        self.speed_homing = 10.
        self.speed_rapid = 50.

    def update_properties(self, **kwargs):
        self.__dict__.update(kwargs)

    def factor(self) -> float:
        return self.steps_per_rev / self.steigung  # [stp / mm]

    def position_legal(self, position:float) -> bool:
        if any([position < self.soft_limits[0],
                position > self.soft_limits[1]]):
            return False
        else:
            return True

    def speed_legal(self, speed:float) -> bool:
        if any([abs(speed) > self.max_speed]):
            return False
        else:
            return True


class Isel_Controller:
    """
        This class enables connection to an ISEL controller via RS-232 in immediate mode.
    """
    def __init__(self, axes:list[Isel_Axis], com_port:str = 'COM4', baud_rate:int=19200, data_bits:int = 8, stop_bits:int = 1):
        # connection properties
        self.connection = None # the connector from pyserial
        self.com_port = com_port # for example /dev/ttyUSB0 , COM{i}
        self.baud_rate = baud_rate # bits per second
        self.data_bits = data_bits # data bits 5 (Baudot code), 6, 7 (ASCII) or 8 (usually)
        self.stop_bits = stop_bits
        # timeouts are set generously to guarantee correct command execution. They may be decreased for faster operation.
        self.read_timeout = 1. # [s]
        self.write_timeout = 1. # [s]

        # It is assumed that the connected axes always occupy the lowest possible ports on the controller.
        # As an example, a single axis would be connected to port 1 ('x' in the documentation),
        # two axes to ports 1 and 2 ('x, y') and so on.
        self.axes = axes
        # config axes
        if test:
            print('Test Mode. No commands will be sent.')

    ## Communication

    def send_command(self, command:str, check_return:bool = True) -> bytes | None:

        if not test:
            self.connection.reset_input_buffer()
            self.connection.reset_output_buffer()
            self.connection.write(bytes(command, 'utf8') + b'\r')
            if check_return:
                while self.connection.in_waiting == 0:
                    time.sleep(0.01)
                ret_val = self.connection.readline()
                if bytes(ret_val[0:1]) in error_codes.keys():
                    print(f'SendCommand: Error on command: {command}')
                    print(f'SendCommand: {_error_check(ret_val)}')
                return ret_val
            else:
                return b'-1'
        else:
            print(f'SendCommand: Command to be sent: {command}')
            return None

    def open(self):
        self.connection = serial.Serial(port = self.com_port,
                                        baudrate = self.baud_rate,
                                        bytesize = self.data_bits,
                                        parity=serial.PARITY_NONE,
                                        stopbits=self.stop_bits,
                                        timeout=self.read_timeout,
                                        write_timeout=self.write_timeout)
        print('Open: ISEL controller communication started: ', self.connection.is_open)
        self.set_axes_config([a.name for a in self.axes])

    def close(self):
        self.connection.close()

    ## Translation for Axis Configuration

    def axis_by_name(self, name:str) -> int:
        """
        Returns the position of an axis in the self.axis list.
        :param name: name of the axis
        :return: the id if axis is found, else -1
        """
        axes_dict = {axis.name: i for i, axis in enumerate(self.axes)}
        if name in axes_dict.keys():
            return axes_dict[name]
        else:
            raise ValueError(f'AxisByName: Axis with name {name} not found.')

    def axes_byte(self, names:str|list[str]) -> str:
        """
        Returns the byte for the serial command that corresponds to the given axes configuration.
        :param names: name or list of names for the chosen axes
        :return: "axis byte"
        """
        if not names:
            return -1
        if type(names) == str:
            names = [names]

        ax_ids = [self.axis_by_name(d) for d in names]
        ax_ids.sort()
        print(tuple(ax_ids))
        switcher = {
            (0,): 1,    # x
            (1,): 2,    # y
            (0,1): 3,   # x, y
            (2,): 4,    # z
            (0,2): 5,   # x, z
            (1,2): 6,   # y, z
            (0,1,2): 7, # x, y, z
            # [3]: 8     # a
        }
        return str(switcher.get(tuple(ax_ids)))

    ## Commands

    def set_axes_config(self, names:list[str], check_return:bool = True):
        """
        Sets the axis configuration of the controller and in the object
        :param names: list of axes names.
        :param check_return: enables check of return code. if set to False, error codes may not be recognized.
        :return: none
        """
        if names is None:
            names = [a.name for a in self.axes]
        ab = self.axes_byte(names)
        self.send_command(f'@0{ab}', check_return=check_return)
        self.axis_config = ab
        print('SetAxisConfig: Current axis configuration set to: ', ','.join(names))

    def home_axes(self, names:list[str], speed_homing:list[float] = None, check_return:bool = True):
        """
        Homes the specified axes. at their set homing position.
        :param names: list of specified axes names.
        :param speed_homing: list of speeds in mm/s to home axes.
        :param check_return: enables check of return code. if set to False, error codes may not be recognized.
        """
        ax_ids = [self.axis_by_name(n) for n in names]
        # set homing speed for all axes
        if speed_homing is None:
            print('HomeAxes: No homing speed given, using defaults.')
            speed_homing_stp = [int(self.axes[a].speed_homing * self.axes[a].factor()) for a in ax_ids]
        else:
            speed_homing_stp = [int(speed_homing[i] * self.axes[a].factor()) for i, a in enumerate(ax_ids)]
            for i, n in enumerate(ax_ids):
                print(f'HomeAxes: Setting homing speed for axis {n}: {speed_homing[i]} mm/s ({speed_homing_stp[i]} stp/s)')
                self.axes[n].update_properties(speed_homing = speed_homing[i])
        command_set_speed = '@0d' + ','.join([str(s) for s in speed_homing_stp])
        self.send_command(command_set_speed, check_return = check_return)

        # home chosen axes
        for n in names:
            ab = self.axes_byte(n)
            print(f'HomeAxes: Homing {n}')
            command_home = '@0R' + str(ab)
            self.send_command(command_home, check_return = check_return)
            print(f'HomeAxes: Homed {n}')
            self.axes[self.axis_by_name(n)].position = 0.

    def move(self, names:list[str], dist:list[float], movement:str = 'abs', round_steps:bool = False, check_return:bool = True, ignore_home:bool = False):
        """
        Move command.
        :param names: list of axes names.
        :param dist: list of distances in mm to move.
        :param movement: type of movement.
            - abs: absolute position relative to the set axis zero
            - rel: position relative to current position.
        :param round_steps: If true, rounds position to nearest reachable step. If false, tries to reach exact
            position and throws warning if unable to do so.
        :param check_return: enables check of return code. if set to False, error codes may not be recognized.
        :param ignore_home: Disable check whether axis is homed when in relative mode.
        """

        # movement types
        mov_type = ['abs', 'rel']
        if movement not in mov_type:
            raise ValueError(f'Move: Movement-type \'{movement}\' is not supported. Must be '+' or '.join(mov_type))

        # get axes indices
        ax_ids = [self.axis_by_name(n) for n in names]

        # unused axes for sending a complete move command
        add_ids = [i for i in range(len(self.axes)) if i not in ax_ids]
        if add_ids != []:
            add_names = [self.axes[a].name for a in add_ids]
            if movement == 'abs':
                add_dist = [self.axes[a].position for a in add_ids]
            elif movement == 'rel':
                add_dist = [0. for _ in range(len(add_ids))]
            else:
                raise ValueError
        else:
            add_names = []
            add_dist = []

        # sort axes
        all_ids, all_names, all_dist = zip(*sorted(zip(ax_ids + add_ids, names + add_names, dist + add_dist)))
        #print(f'Move: Sorted axes: {all_ids, all_names, all_dist}')

        # positions
        p_old = [self.axes[a].position for a in all_ids]
        if movement == 'abs':
            p_new_th = all_dist
            p_diff = [new - old for new, old in zip(p_new_th, p_old)]
        elif movement == 'rel':
            p_new_th = [p + d for p, d in zip(p_old, dist)]
            p_diff = all_dist
        else:
            raise ValueError

        #round positions to nearest whole step number
        if round_steps:
            mm_per_step = [1. / self.axes[a].factor() for a in all_ids]
            p_new_th = [mmpstp * np.round(p / mmpstp) for p, mmpstp in zip(p_new_th, mm_per_step)]
            p_diff = [mmpstp * np.round(p / mmpstp) for p, mmpstp in zip(p_diff, mm_per_step)]

        # safety interlocks
        for a, d in zip(all_ids, p_new_th):
            if a in ax_ids:
                # Homing: Axes need to be homed to move.
                # (except if movement is relative and command is given to ignore homing status)
                if self.axes[a].position is None:
                    if movement == 'abs' or (movement == 'rel' and not ignore_home):
                        raise ValueError(f'Move: Axis \'{self.axes[a].name}\' needs to be homed before moving!')

                # Soft Limits: Position must not exceed soft limits of the axis.
                if not self.axes[a].position_legal(d):
                    raise ValueError(f'Move: New position {d} mm on axis \'{self.axes[a].name}\' out of bounds!')

                # Precision: Position has to be reachable with the stepsize of the motors.
                if not round_steps:
                    mm_per_stp = 1. / self.axes[a].factor()
                    eps = 1e-4
                    rel_error = min(abs((d % mm_per_stp)/mm_per_stp), abs((d % mm_per_stp)/mm_per_stp -1. ))
                    if rel_error > eps:
                        raise ValueError(f'Move: New position {d} mm on axis \'{self.axes[a].name}\' not reachable at required precision. Position needs to be a positive integer multiple of {mm_per_stp} mm! Consider rounding to nearest step with round_steps!')

        # check if movement is necessary
        if all([p == 0. for p in p_diff]):
            print('Move: Axes already at desired location')
        else:
            # steps to new position + movement command
            if movement == 'abs':
                steps = [int(self.axes[a].factor() * pos) for a, pos in zip(all_ids, p_new_th)]
                command = '@0M'
            elif movement == 'rel':
                steps = [int(self.axes[a].factor() * pos) for a, pos in zip(all_ids, p_diff)]
                command = '@0A'
            # movement speed
            speeds = [int(self.axes[a].factor() * self.axes[a].speed) for a in all_ids]


            # build command
            params = []
            for s, v in zip(steps, speeds):
                params += [str(s), str(v)]
            command += ','.join(params)
            # send command
            self.send_command(command, check_return=check_return)


            #check position accuracy
            factors = [a.factor() for a in self.axes]
            while len(factors) < 3:
                factors += [-1.]
            steps_ac = self.get_current_steps()
            p_new_ac = [s / fac for s, fac in zip(steps_ac, factors)]
            for a, p_a, p_t in zip(all_ids, p_new_ac, p_new_th):
                self.axes[a].update_properties(position=p_a)
                print(f'Move: New Position for {self.axes[a].name}: {p_a} mm')
                if p_t != p_a:
                    print(f'Move: Unable to reach exact position on axis {self.axes[a].name}: {p_t} mm!')


    def get_current_steps(self, names:list[str] = None) -> list[int]:
        """
        Returns the current steps from the home position for all axes.
        :param names: list of axes of which to return the position. If none are given, all positions are returned.
        """
        ret_val = self.send_command('@0P')[1:] #
        #print(ret_val)
        positions = [hexb2int(ret_val[0:6]),
                     hexb2int(ret_val[6:12]),
                     hexb2int(ret_val[12:18])]

        if names is not None:
            ax_ids = [self.axis_by_name(n) for n in names]
            return [positions[a] for a in ax_ids]
        else:
            return positions