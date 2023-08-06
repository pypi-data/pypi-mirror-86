from collections import namedtuple
import datetime
import copy

import dateutil.parser
import numpy as np
from scipy import interpolate

from drama import constants as const
from drama.geo import geometry as geo
from drama.io import cfg
from drama.orbits import sunsync_orbit as sso
from drama.utils import misc as misc


# from drama.orbits import repeat_design as rd

__author__ = "Paco Lopez Dekker"
__email__ = "F.LopezDekker@tudeft.nl"

Orbit = namedtuple(
    "Orbit",
    ["r_ecef", "v_ecef", "Horb", "asc_idx", "desc_idx", "aei", "timevec"],
)


class KeplerianOrbit(object):
    """KepplerianOrbit holds attributes related to the Kepplerian
    parameters of an orbit around a body. It uses the attributes to
    calculate the position and velocity of the body along the orbit.

    Parameters
    ----------
    e :
        eccentricity
    a :
        semi-major axis [m]
    i :
        inclination [deg]
    omega :
        argument of perigee
    asc_node :
        right ascension of the ascending node [deg]
    accuracy :
        param r_planet: radius of planet (defaults to Earth)
    gm_planet :
        mass of planet (defaults to Earth)
    interval :
        time over which we calculate orbit, in seconds
    param perigee_drift:
        if set to False we assume perigee is maintained, otherwise it drifts naturally
        orbit maintenance
    """

    def __init__(
        self,
        e,
        a,
        i,
        omega,
        asc_node=0.0,
        accuracy=1e-08,
        r_planet=const.r_earth,
        gm_planet=const.gm_earth,
        interval=None,
        timestep=1.0,
        starttime=0.0,
        offset_time=0.0,
        adjust_ascending_node=True,
        verbose=False,
        perigee_drift=False,
    ):
        """
        Initialise a KeplerianOrbit.
        """
        self.__init_done = False
        self.e = e
        self.a = a
        self.i = i
        self.omega = omega
        self.asc_node = asc_node
        self.accuracy = accuracy
        self.r_planet = r_planet
        self.gm_planet = gm_planet
        self.verbose = verbose

        # Initialize derived parameters
        self.asc_node_dot = self.nodal_regression("j4")  # [rad/sec]
        if perigee_drift:
            self.omega_per_dot = self.omega_per_dot("j2")  # [rad/sec]
        else:
            self.omega_per_dot = 0
        # Mean angular motion
        self.n0 = np.sqrt(const.gm_earth / (self.a ** 3.0))
        # Calculate Orbital Period & mean motion
        self.n0 = np.sqrt(const.gm_earth / (a ** 3.0))
        self.period = 2 * np.pi / self.n0
        # timeduration = None, timestep = 1, starttime = 0
        if interval is None:
            # Do one orbit
            self.interval = self.period
        else:
            self.interval = interval
        self.timestep = timestep
        self.starttime = starttime
        self.offset_time = offset_time
        self.adjust_ascending_node = adjust_ascending_node
        # Init output variables just to avoid warnings
        self.timevec = None
        self.reci = None
        self.recf = None
        self.veci = None
        self.vecf = None
        self.AE = None
        self.AM = None
        self.vel_abs = None
        self.r_abs = None
        self.anomaly = None
        self.u_all = None
        self.r_all = None
        self.lon_arr = None
        self.lat_att = None
        self.velocity_vec = None
        self.__init_done = True
        self.__calc_orb()

    @property
    def asc_node(self):
        """ """
        return self.__asc_node

    @asc_node.setter
    def asc_node(self, asc_node):
        self.__asc_node = asc_node
        # Update orbit
        if self.__init_done:
            self.__calc_orb()

    @property
    def timestep(self):
        return self.__timestep

    @timestep.setter
    def timestep(self, timestep):
        self.__timestep = timestep
        # Update orbit
        if self.__init_done:
            self.__calc_orb()

    @property
    def starttime(self):
        return self.__starttime

    @starttime.setter
    def starttime(self, starttime):
        self.__starttime = starttime
        # Update orbit
        if self.__init_done:
            self.__calc_orb()

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, interval):
        self.__interval = interval
        # Update orbit
        if self.__init_done:
            self.__calc_orb()

    @property
    def period(self):
        return self.__period

    @period.setter
    def period(self, period):
        self.__period = period
        self.n0 = 2 * np.pi / self.__period
        # Update orbit
        if self.__init_done:
            self.__calc_orb()

    def nodal_regression(self, accuracy="j4"):
        """Calculate the nodal regression for certain orbit parameters

        Parameters
        ----------
        accuracy :
            j2 or j4 (Default value = "j4")

        Returns
        -------
        type
            nodal regression [rad/s]

        """
        # define constants
        r_earth = self.r_planet
        gm_earth = self.gm_planet
        j2 = const.j2
        j4 = const.j4

        i_rad = np.deg2rad(self.i)
        n = np.sqrt(
            gm_earth / (self.a ** 3)
        )  # angular velocity, mean motion [rad/s]
        p = self.a * (1 - self.e ** 2)  # semi-latus rectum

        if accuracy == "j2":
            asc_node_dot = (
                -3 * n * (r_earth ** 2) * j2 * np.cos(i_rad) / (2 * p ** 2)
            )

        else:
            t1 = -3 * n * (r_earth ** 2) * j2 * np.cos(i_rad) / (2 * p ** 2)

            t2 = (
                3
                * n
                * (r_earth ** 4)
                * (j2 ** 2)
                * np.cos(i_rad)
                / (32.0 * p ** 4)
            ) * (
                12
                - 4 * self.e ** 2
                - (80 + 5 * self.e ** 2) * (np.sin(i_rad) ** 2)
            )

            t3 = (
                15 * n * (r_earth ** 4) * j4 * np.cos(i_rad) / (32.0 * p ** 4)
            ) * (
                8
                + 12 * self.e ** 2
                - (14 + 21 * self.e ** 2) * (np.sin(i_rad) ** 2)
            )
            asc_node_dot = t1 + t2 + t3
        return asc_node_dot

    def omega_per_dot(self, accuracy="j4"):
        """Calculates argument of perigee drift

        Parameters
        ----------
        accuracy :
            j2 or j4 (Default value = "j4")

        Returns
        -------
        float
            drift of argument of perigee [rad/s]

        """
        r_earth = self.r_planet
        gm_earth = self.gm_planet
        j2 = const.j2
        j4 = const.j4
        i = self.i
        e = self.e
        a = self.a
        i_rad = np.deg2rad(i)
        n = np.sqrt(gm_earth / (a ** 3))  # mean motion
        p = a * (1 - e ** 2)  # semi-latus rectum

        if accuracy == "j2":
            omega_per_dot = (
                (3.0 / 4)
                * n
                * j2
                * ((r_earth / p) ** 2)
                * (4.0 - 5.0 * (np.sin(i_rad)) ** 2)
            )

        else:
            t1 = (
                (3.0 / 4)
                * n
                * j2
                * ((r_earth / p) ** 2)
                * (4.0 - 5.0 * (np.sin(i_rad)) ** 2)
            )

            t2 = (
                (9.0 / 384)
                * n
                * (j2 ** 2)
                * ((r_earth / p) ** 4)
                * (
                    56.0 * e ** 2
                    + (760.0 - 36.0 * e ** 2) * ((np.sin(i_rad)) ** 2)
                    - (890.0 + 45.0 * e ** 2) * ((np.sin(i_rad)) ** 4)
                )
            )

            t3 = (
                (-15.0 / 128)
                * n
                * j4
                * ((r_earth / p) ** 4)
                * (
                    64.0
                    + 72.0 * e ** 2
                    - (248.0 + 252.0 * e ** 2) * ((np.sin(i_rad)) ** 2)
                    + (196.0 + 189.0 * e ** 2) * ((np.sin(i_rad)) ** 4)
                )
            )

            omega_per_dot = t1 + t2 + t3

        return omega_per_dot

    def __calc_orb(self, verbose=False):

        # define constants
        omega_earth = const.omega_earth  # omega earth

        # Print Parameters
        if verbose:
            print(" Parameters:     ")
            print(" -----------     ")
            print(" Inclination:    ", self.i, "deg")
            print(" Semi major:     ", self.a, "m")
            print(" Above Ground:   ", (self.a - self.r_planet), "m")
            print(" Eccentricity:   ", self.e)
            print(" Ascend. Node:   ", self.asc_node, "deg")
            print(" Arg. of Perigee:", self.omega, "deg")
            print(" Starttime:      ", self.starttime)
            print(" Duration:       ", self.interval, "days")
            print(" Time increment: ", self.timestep)
            print(" Offset Time:    ", self.offset_time)

        [i_rad, asc_node_rad0, omega_rad0] = np.deg2rad(
            [self.i, self.asc_node, self.omega]
        )

        timeduration = self.interval  # timeduration in seconds
        # get 5 more values for calc. velocity etc.
        offset = 3
        starttime = self.starttime
        timestep = self.timestep
        omega_per_dot = self.omega_per_dot
        tottime = starttime - (offset * timestep)
        numpoints = (
            int(np.ceil(timeduration / timestep)) + offset
        )  # extra values
        timevec = np.arange(numpoints) * timestep + tottime

        # solve angle with Newtonian algorithm for each point
        # ascending node and argument of perigee after adding orbital
        # pertubation effects
        omega_rad = omega_rad0 + omega_per_dot * timevec

        # Mean anomaly; changes by 360 degrees during one revolution
        M = np.mod((self.n0 * timevec), (2.0 * np.pi))
        Ep = M  # Previous eccentric anomaly (here initial state)
        delta_E = np.ones(numpoints)
        # Eccentric anomaly difference (to check convergence)

        # check for convergence
        while delta_E.max() >= self.accuracy:
            # Eccentric Anomaly of next state
            En = Ep - (
                (Ep - (self.e * np.sin(Ep)) - M) / (1.0 - (self.e * np.cos(Ep)))
            )
            # Update difference
            delta_E = np.abs(En - Ep)
            Ep = En

        # true anomaly
        true_anom = np.arctan2(
            (np.sqrt(1.0 - (self.e ** 2.0)) * np.sin(En)), (np.cos(En) - self.e)
        )

        AE = En  # Eccentric Anomaly
        AM = M  # Mean anomaly

        u_all = np.mod((omega_rad + AM), (2.0 * np.pi))

        # orbit radius
        r = (
            self.a
            * (1.0 - (self.e ** 2.0))
            / (1.0 + (self.e * np.cos(true_anom)))
        )

        asc_node_ = self.asc_node + timevec * self.asc_node_dot  # [deg]

        # Finding Velociy
        asc_node_rad2 = np.deg2rad(asc_node_)
        f = np.sqrt(const.gm_earth * self.a) / (
            self.a * (1.0 - self.e * np.cos(true_anom))
        )

        # unit vector pointing towards the perigee
        P = np.array(
            [
                [
                    np.cos(omega_rad0) * np.cos(asc_node_rad2)
                    - np.sin(omega_rad0) * np.cos(i_rad) * np.sin(asc_node_rad2)
                ],
                [
                    np.cos(omega_rad0) * np.sin(asc_node_rad2)
                    + np.sin(omega_rad0) * np.cos(i_rad) * np.cos(asc_node_rad2)
                ],
                [
                    np.sin(omega_rad0)
                    * np.sin(i_rad)
                    * np.ones(len(asc_node_rad2))
                ],
            ],
            dtype="float",
        )

        # unit vector corresponding to true anomaly of 90 degrees
        Q = np.array(
            [
                [
                    -np.sin(omega_rad0) * np.cos(asc_node_rad2)
                    - np.cos(omega_rad0) * np.cos(i_rad) * np.sin(asc_node_rad2)
                ],
                [
                    -np.sin(omega_rad0) * np.sin(asc_node_rad2)
                    + np.cos(omega_rad0) * np.cos(i_rad) * np.cos(asc_node_rad2)
                ],
                [
                    np.cos(omega_rad0)
                    * np.sin(i_rad)
                    * np.ones(len(asc_node_rad2))
                ],
            ],
            dtype="float",
        )

        # Velocity vector ECI
        veci = -f * (
            (np.sin(true_anom)) * P
            - np.sqrt(1 - self.e ** 2) * np.cos(true_anom) * Q
        )
        veci = veci.reshape(3, timevec.shape[0]).T

        # Position vector ECI
        reci = (
            self.a * (np.cos(true_anom) - self.e) * P
            + self.a * np.sqrt(1 - self.e ** 2) * np.sin(true_anom) * Q
        )
        reci = reci.reshape(3, timevec.shape[0]).T

        # rotate velocity vector:
        ang_tmp = np.rad2deg(omega_earth * (timevec + self.offset_time))
        velocity_vec = geo.rot_z(veci, ang_tmp).T

        # declination (gamma)
        latitude = np.arctan(
            reci[:, 2] / (np.sqrt((reci[:, 0] ** 2.0) + (reci[:, 1] ** 2.0)))
        )
        # PLD now I am going to find the time of ascending node
        if self.adjust_ascending_node:
            ## This assumes that timevec is long enough to include the ascending node
            eq_cross_ind = np.where(
                np.logical_and(latitude[1:] >= 0, latitude[0:-1] < 0)
            )
            if eq_cross_ind[0].size == 0:
                print(
                    "calc_orbit: No ascending node could be found, the time vector was probably to short"
                )
                dt_asc_node = 0
            else:
                dt_asc_node = timevec[eq_cross_ind[0][0]]  # - timevec[0]

        # rotate position and velocity vectors to ECEF reference frame
        alpha = (self.offset_time - dt_asc_node) * omega_earth
        argR = np.rad2deg(omega_earth * timevec + alpha)
        recf = geo.rot_z(reci, argR).T
        vecf = (
            geo.rot_z(veci, argR).T
            + omega_earth * geo.rot_z_prime(reci, argR).T
        )

        # right ascension (alpha)
        longitude = np.arctan2(reci[:, 1], reci[:, 0])

        # Due to earth rotation: modify longitude
        longitude = longitude - omega_earth * (
            timevec + self.offset_time - dt_asc_node
        )

        # To ensure that longitude lies within valid range
        longitude = np.arctan2(np.sin(longitude), np.cos(longitude))

        # Outputs
        lon_arr = np.rad2deg(longitude)
        lat_arr = np.rad2deg(latitude)

        # geocentric distance
        r_abs = np.sqrt(
            reci[:, 0] ** 2.0 + reci[:, 1] ** 2.0 + reci[:, 2] ** 2.0
        )

        # absolute velocity relative to Earth
        vel_abs = np.sqrt(const.gm_earth * (2.0 / r_abs - 1.0 / self.a))

        # cut back arrays to exact repeat cycle (remove additional time steps)
        timevec = timevec[offset:]

        reci = reci[offset:, :]
        recf = recf[offset:, :]
        veci = veci[offset:, :]
        vecf = vecf[offset:, :]
        velocity_vec = velocity_vec[offset:, :]
        AE = AE[offset:]
        AM = AM[offset:]
        vel_abs = vel_abs[offset:]
        r_abs = r_abs[offset:]
        true_anom = true_anom[offset:]
        u_all = u_all[offset:]
        r_all = r[offset:]
        lon_arr = lon_arr[offset:]
        lat_arr = lat_arr[offset:]
        self.timevec = timevec
        self.reci = reci
        self.recf = recf
        self.veci = veci
        self.vecf = vecf
        self.AE = AE
        self.AM = AM
        self.vel_abs = vel_abs
        self.r_abs = r_abs
        self.anomaly = np.degrees(true_anom)
        self.u_all = u_all
        self.r_all = r_all
        self.lon_arr = lon_arr
        self.lat_att = lat_arr
        self.velocity_vec = velocity_vec


class SingleOrbit(object):
    """SingleOrbit holds attributes relevant to one orbit, and calculates
    the position and velocity of the body based on the Keplerian
    model.

    Parameters
    ----------
    conffile : str
        name of configuration file
    conftuple : str
        name of configuration file (overrides conffile)
    aei : tuple
        tuple with semi-major axis, eccentricity, and inclination
    orb_type : str, optional
        choose between sunsync and repeat orbit, defaults to "sunsync".
    """

    def __init__(
        self,
        conffile=None,
        conftuple=None,
        aei=None,
        orb_type="sunsync",
        perigee_drift=False,
        comp_dasc_node=0.0,
        companion_delay=0.0,
    ):
        """
        Initialise a SingleOrbit.
        """
        if conftuple is None:
            conffile = misc.get_par_file(conffile)
            self.conf = cfg.ConfigFile(conffile)
        else:
            self.conf = conftuple
        T_sidereal = 86164.09053
        ndays = self.conf.orbit.days_cycle
        nrevs = self.conf.orbit.orbits_nbr
        # for backward compatibility
        self.norb = nrevs
        self.n_current_orbit = 0
        self.repeat_cycle = ndays
        if type(aei) is tuple:
            (self.a, self.e, self.i) = aei
            if orb_type == "sunsync":
                # Generate parameters for sunsync orbit
                self.Torb = 24.0 * ndays / nrevs  # orbital period [hrs]
            elif orb_type == "repeat":
                Tao = float(ndays) / nrevs
                self.Torb = T_sidereal * Tao
        elif orb_type == "sunsync":
            # Generate parameters for sunsync orbit
            self.Torb = 24.0 * ndays / nrevs  # orbital period [hrs]
            (self.a, self.e, self.i) = sso.get_sunsync_repeat_orbit(
                ndays, nrevs, silent=True
            )
        elif orb_type == "repeat":
            # Aquire repeat specific orbit params
            print("Repeat orbit design deprecated, for now")
        else:
            print("Should never be here!")

        self._track_direction = "complete"
        # For backward compatibility
        self.aei = (self.a, self.e, self.i)
        # Invent an arbitrary time stamp
        # FIXME
        self.T0 = dateutil.parser.parse("2014-12-05T07:57:25.000000Z")
        if hasattr(self.conf.orbit, "ltan"):
            self.T0 = dateutil.parser.parse(self.conf.orbit.ltan)
        self.Horb = self.a - const.r_earth
        self.perigee_drift = perigee_drift
        self.comp_dasc_node = comp_dasc_node
        self.companion_delay = companion_delay
        # The following variables are set in __calc_orbit(), they
        # don't need to be initialised here.
        # self.companion = False
        # self.asc_node_c = 0
        # self._timevec = None
        # self.asc_idx = None
        # self.desc_idx = None
        # self.r_ecef = None
        # self._v_ecef = None
        self.timestep = self.conf.orbit.timestep  # [s]
        self.starttime = 0
        # self.t_orb = None
        # Compute orbit. This is encapsulated in a private function to allow extending to external orbits
        self.asc_node = self.conf.orbit.asc_node
        self.__calc_orbit()

    @property
    def track_direction(self):
        """Determine if the swath is for the complete, ascending,
        or descending part of the orbit.

        Possible values: 'ascending', 'descending', 'complete'
        """
        return self._track_direction

    @track_direction.setter
    def track_direction(self, value):
        if value not in {"ascending", "descending", "complete"}:
            raise ValueError(
                "Possible values: 'ascending', 'descending', 'complete'"
            )
        self._track_direction = value

    @property
    def v_ecef(self):
        if self._track_direction == "complete":
            return self._v_ecef
        elif self._track_direction == "ascending":
            return self._v_ecef[self.asc_idx[0] : (self.asc_idx[1] + 1), :]
        else:
            return self._v_ecef[self.desc_idx[0] : (self.desc_idx[1] + 1), :]

    @property
    def timevec(self):
        if self._track_direction == "complete":
            return self._timevec
        elif self._track_direction == "ascending":
            return self._timevec[self.asc_idx[0] : (self.asc_idx[1] + 1)]
        else:
            return self._timevec[self.desc_idx[0] : (self.desc_idx[1] + 1)]

    def __iter__(self):
        return self

    def __next__(self):
        if self.n_current_orbit > self.norb:
            raise StopIteration
        else:
            delta_ascending_node = self.angular_precession_per_orbit()
            results = copy.deepcopy(self.results)
            self.asc_node += np.rad2deg(delta_ascending_node)
            self.starttime += self.t_orb
            self.__calc_orbit()
            self.n_current_orbit += 1
            return results

    def __calc_orbit(self):
        # inData = self.conf
        a = self.a
        e = self.e
        i = self.i
        omega = self.conf.orbit.omega_p

        # Calculate period of one orbit
        n0 = np.sqrt(const.gm_earth / (a ** 3))  # mean motion
        orbit_period = 2 * np.pi / n0  # orbital period [s]
        self.t_orb = orbit_period
        timeduration = orbit_period + self.starttime  # [s]
        keporb = KeplerianOrbit(
            e,
            a,
            i,
            omega,
            asc_node=self.asc_node,
            interval=timeduration,
            timestep=self.timestep,
            starttime=self.starttime,
            perigee_drift=self.perigee_drift,
        )
        keporb.interval = keporb.period * 2  # just to be save
        anomaly0 = np.angle(np.exp(1j * np.radians(keporb.omega))) / (
            2 * np.pi
        )  # in cycles
        keporb.starttime = -keporb.period * (0.4 + anomaly0)
        self.keporb = keporb
        dao = np.radians(self.comp_dasc_node) * a

        if (self.companion_delay != 0) or (dao != 0):
            self.companion = True
            asc_node_c = (
                self.asc_node
                - self.companion_delay * 360 / 86400
                + np.degrees(dao / a)
            )
        else:
            self.companion = False
            asc_node_c = self.asc_node
        self.asc_node_c = asc_node_c
        v_indices = misc.asc_desc(keporb.vecf)
        asc_idx = v_indices.asc_idx
        desc_idx = v_indices.desc_idx
        self._timevec = keporb.timevec[asc_idx[0, 0] : asc_idx[1, 0]]
        self.asc_idx = asc_idx[0] - asc_idx[0, 0]
        self.desc_idx = desc_idx[1] - asc_idx[0, 0]
        if self.companion:
            keporb.asc_node = self.asc_node_c
            keporb.starttime = (
                -keporb.period * (0.4 + anomaly0) - self.companion_delay
            )
        self.r_ecef = keporb.recf[asc_idx[0, 0] : asc_idx[1, 0]]
        self._v_ecef = keporb.vecf[asc_idx[0, 0] : asc_idx[1, 0]]
        self.T0 = self.T0 + datetime.timedelta(seconds=self._timevec[0])
        self._timevec = self._timevec - self._timevec[0]
        self.results = Orbit(
            self.r_ecef,
            self._v_ecef,
            self.Horb,
            self.asc_idx,
            self.desc_idx,
            self.aei,
            self._timevec,
        )

    def angular_precession_per_orbit(self, radius_planet=const.r_earth):
        """
        Parameters
        ----------
        radius_planet : float
            Radius of planet considered [m], (Default value = const.r_earth)

        Returns
        -------
        out : float
            change in the longitude of the ascending node per one
            orbit around an oblate planet [rad]
        """
        i_rad = np.deg2rad(self.i)
        latus_rectum = self.a * (1 - self.e ** 2)  # semi-latus rectum
        delta_ascending_node = (
            -3
            * np.pi * (const.j2 * radius_planet ** 2)
            * np.cos(i_rad) / (latus_rectum ** 2)
        )
        # Only uncomment the following print statements for debugging
        #print('before rotation of the Earth', np.rad2deg(delta_ascending_node))

        # subtract the the rotation of the Earth from the angular
        # precession
        delta_ascending_node = delta_ascending_node - (self.Torb * 3600 * const.omega_earth)

        #print('after rotation of the Earth', np.rad2deg(delta_ascending_node))
        #print('orbital period is ', self.Torb * 60)
        #print('in orbit ', self.n_current_orbit)
        return delta_ascending_node

    def interp_orbit(self, t):
        """Compute orbit position and speed at a specific time through simple
        interpolation on the pre-computed orbit samples

        Parameters
        ----------
        t :
            time of interpolation

        Returns
        -------
        ndarray
            interpolated r_ecef, interpolated v_ecef

        """
        r_x_interp = interpolate.interp1d(
            self.timevec, self.r_ecef[:, 0], kind="cubic"
        )
        r_y_interp = interpolate.interp1d(
            self.timevec, self.r_ecef[:, 1], kind="cubic"
        )
        r_z_interp = interpolate.interp1d(
            self.timevec, self.r_ecef[:, 2], kind="cubic"
        )
        v_x_interp = interpolate.interp1d(
            self.timevec, self.v_ecef[:, 0], kind="cubic"
        )
        v_y_interp = interpolate.interp1d(
            self.timevec, self.v_ecef[:, 1], kind="cubic"
        )
        v_z_interp = interpolate.interp1d(
            self.timevec, self.v_ecef[:, 2], kind="cubic"
        )

        r_ecef_int = np.array([r_x_interp(t), r_y_interp(t), r_z_interp(t)]).T
        v_ecef_int = np.array([v_x_interp(t), v_y_interp(t), v_z_interp(t)]).T

        return r_ecef_int, v_ecef_int
