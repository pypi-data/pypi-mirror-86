from __future__ import annotations

import contextlib
import functools
import io
import logging
import pathlib
import tempfile

import numpy as np

from . import opensees as ops

#===============================================================================
# Globals
#===============================================================================
__all__ = [
    'areaCircularSector',
    'captureOutput',
    'centroidCircularSector',
    'fillOutNumbers',
    'fourFiberSectionGJ',
    'getClassLogger',
    'linspaceCoords2d',
    'linspaceCoords3d',
    'nShapesCentroid',
    'patchRect2d',
    'patchHalfCircTube2d',
    'scratchFileFactory',
    'twoFiberSection',
    'updateRayleighDamping',
]

logger = logging.getLogger(__name__)


#===============================================================================
# Utilities
#===============================================================================
def getClassLogger(cls) -> logging.Logger:
    """Get a logger scoped to the requested class.

    Parameters
    ----------
    cls : type
        Class to get a logger for.

    Example
    -------
    >>> class ClassWithLogger():
    ...     def __init__(self):
    ...         self.logger = getClassLogger(self.__class__)
    ...     def some_func(self, msg):
    ...         self.logger.warning(msg)
    ...
    >>> logging.basicConfig(format='%(name)s.%(funcName)s: %(message)s')
    >>> instance = ClassWithLogger()
    >>> instance.some_func('this is a warning')
    __main__.ClassWithLogger.some_func: this is a warning
    """
    return logging.getLogger(cls.__module__ + '.' + cls.__name__)


def scratchFileFactory(analysisName, scratchPath=None, analysisID=0):
    """Create a scratch file path generator.

    Parameters
    ----------
    analysisName : str
        Name of the analysis, e.g. 'SectionAnalysis'.
    scratchPath : path_like
        Path to the scratch directory. If None, uses the system temp directory.
        (default: None)
    analysisID : optional
        Unique ID for the analysis. Useful for parallel execution, for example.
        (default: 0)

    Returns
    -------
    scratchFile
        A function that takes two arguments, 'name' and 'suffix'.

    Example
    -------
    >>> scratchFile = scratchFileFactory('TestoPresto')
    >>> scratchFile('disp', '.dat')
    PosixPath('/tmp/TestoPresto_disp_0.dat')
    """
    if scratchPath is None:
        scratchPath = tempfile.gettempdir()
    scratchPath = pathlib.Path(scratchPath).resolve()

    def scratchFile(name, suffix='') -> pathlib.Path:
        """
        Parameters
        ----------
        name : str
            Name of the scratch file, e.g. 'displacement'.
        suffix : str, optional
            Suffix to use for the scratch file. (default: '')
        """
        return scratchPath/f'{analysisName}_{name}_{analysisID}{suffix}'

    return scratchFile


class OpenSeesAnalysis():
    def __init__(self, scratchPath=None, analysisID=None):
        self.logger = getClassLogger(self.__class__)
        self.scratchFile = scratchFileFactory(self.__class__.__name__,
                                              scratchPath, analysisID)
        self.deleteFiles = True


def updateRayleighDamping(modeA, ratioA, modeB, ratioB,
                          solver='-genBandArpack'):
    """Run an eigenvalue analysis and set proportional damping based on the
    current state of the structure.

    Parameters
    ----------
    modeA : int
        First specified mode with prescribed damping.
    ratioA : float
        Damping ratio prescribed for mode A.
    modeB : int
        Second specified mode with prescribed damping.
    ratioB : float
        Damping ratio prescribed for mode B.
    solver : {'-genBandArpack', '-symmBandLapack', '-fullGenLapack'}, optional
        Solver to use for the eigenvalue analysis. (default: '-genBandArpack')
    """
    # Get natural frequencies at the desired modes
    maxMode = modeA if modeA > modeB else modeB
    eigenvalues = ops.eigen(solver, maxMode)
    frequencyA = np.sqrt(eigenvalues[modeA - 1])
    frequencyB = np.sqrt(eigenvalues[modeB - 1])

    # Compute the damping factors
    k = 2.0/(frequencyA**2 - frequencyB**2)
    aM = k*frequencyA*frequencyB*(ratioB*frequencyA - ratioA*frequencyB)
    aK = k*(ratioA*frequencyA - ratioB*frequencyB)
    ops.rayleigh(aM, 0.0, 0.0, aK)


#===============================================================================
# Centroids and things
#===============================================================================
def areaCircularSector(d, R):
    theta = 2*np.arccos(np.abs(d)/R)
    area = 0.5*R**2*(theta - np.sin(theta))
    return area


def centroidCircularSector(d, R):
    theta = 2*np.arccos(np.abs(d)/R)
    # NumPy sign gives 0.0 for zeroes, but we want zeroes to be positive. True
    # gets cast to 1.0, and False to 0.0.
    sign = np.sign(d) + (d == 0.0)
    if theta == 0.0:
        centroid = sign*R
    else:
        centroid = sign*4*R*np.sin(0.5*theta)**3/(3*(theta - np.sin(theta)))
    return centroid


def nShapesCentroid(x, y, A):
    """Calculates the centroid of a group of shapes.

    Parameters
    ----------
    x : array_like
        x-coordinates of the centroids of the shapes.
    y : array_like
        y-coordinates of the centroids of the shapes.
    A : array_like
        Areas of the shapes.

    Returns
    -------
    xbar
        x-coordinate of the centroid.
    ybar
        y-coordinate of the centroid.
    A
        Total area of the group.

    Raises
    ------
    ValueError
        if `x`, `y`, and `A` are not the same size.
    """
    x = np.asanyarray(x).reshape(-1)
    y = np.asanyarray(y).reshape(-1)
    A = np.asanyarray(A).reshape(-1)
    if x.size != y.size or x.size != A.size:
        raise ValueError('nShapesCentroid: x, y, A must be the same size')

    xArea = x.dot(A)
    yArea = y.dot(A)
    area = np.sum(A)
    logger.debug(f'xArea={xArea:g}, yArea={yArea:g}, area={area:g}')

    return xArea/area, yArea/area, area


def fillOutNumbers(peaks, rate):
    """Fill in numbers between peaks.

    Parameters
    ----------
    peaks : array_like
        Peaks to fill between.
    rate : float
        Rate to use between peaks.

    Examples
    --------
    >>> fillOutNumbers([0, 1, -1], rate=0.25)
    array([ 0.  ,  0.25,  0.5 ,  0.75,  1.  ,  0.75,  0.5 ,  0.25,  0.  ,
           -0.25, -0.5 , -0.75, -1.  ])
    >>> fillOutNumbers([[0, 1, -1], [1, 2, -2]], rate=0.25)
    array([[ 0.  ,  1.  , -1.  ],
           [ 0.25,  1.25, -1.25],
           [ 0.5 ,  1.5 , -1.5 ],
           [ 0.75,  1.75, -1.75],
           [ 1.  ,  2.  , -2.  ]])

    Ported from the MATLAB function written by Mark Denavit.
    """
    peaks = np.asanyarray(peaks)

    if len(peaks.shape) == 1:
        peaks = peaks.reshape(peaks.size, 1)

    if peaks.shape[0] == 1:
        peaks = peaks.T

    numpeaks = peaks.shape[0]
    numbers = [peaks[0, :]]

    for i in range(numpeaks - 1):
        diff = peaks[i + 1, :] - peaks[i, :]
        numsteps = int(np.maximum(2, 1 + np.ceil(np.max(np.abs(diff/rate)))))
        numbers_to_add = np.linspace(peaks[i, :], peaks[i + 1, :], numsteps)
        numbers.append(numbers_to_add[1:, :])

    numbers = np.vstack(numbers)
    if 1 in numbers.shape:
        numbers = numbers.flatten()

    return numbers


def linspaceCoords2d(xi,
                     yi,
                     xj,
                     yj,
                     numElements,
                     iOffset=0.0,
                     jOffset=0.0,
                     offsetFactor=False,
                     imperf=0.0):
    """Generate evenly-spaced coordinates for a 2D member, with optional rigid
    offset and sinusoidal imperfection calculation.

    Parameters
    ----------
    xi
        x-coordinate of the i workpoint.
    yi
        y-coordinate of the i workpoint.
    xj
        x-coordinate of the j workpoint.
    yj
        y-coordinate of the j workpoint.
    numElements
        Number of elements.
    iOffset : float, optional
        Distance from the i workpoint to the first coordinate. (default: 0.0)
    jOffset : float, optional
        Distance from the j workpoint to the last coordinate. (default: 0.0)
    offsetFactor : bool, optional
        If True, `iOffset` and `jOffset` specify offsets as a factor of the
        workpoint-to-workpoint length instead of absolute lengths. (default:
        False)
    imperf : float, optional
        Sinusoidal imperfection as a factor of the i-node to j-node length.
        Positive is in the counter-clockwise direction from the vector pointing
        from (`xi`, `yi`) to (`xj`, `yj`). (default: 0.0)

    Returns
    -------
    coords : np.ndarray
        2-d array with x-coordinates in the first row and y-coordinates in the
        second row. Can be unpacked as ``x, y = linspaceCoords2d(*args)``.
    """
    # Plop out x- and y-coordinates on a line, and then rotate/translate into place.
    L = ((xj - xi)**2 + (yj - yi)**2)**0.5
    if offsetFactor:
        iOffset = iOffset*L
        jOffset = jOffset*L
    L -= iOffset + jOffset
    xCoords = iOffset + np.linspace(0, L, numElements + 1)
    yCoords = imperf*L*np.sin(np.pi*(xCoords - iOffset)/L)

    alpha = np.arctan2(yj - yi, xj - xi)
    R = np.array([[np.cos(alpha), -np.sin(alpha)],
                  [np.sin(alpha), +np.cos(alpha)]])

    coords = R @ np.vstack((xCoords, yCoords))
    coords[0, :] += xi
    coords[1, :] += yi

    return coords


def linspaceCoords3d(xi: float,
                     yi: float,
                     zi: float,
                     xj: float,
                     yj: float,
                     zj: float,
                     numElements: int,
                     iOffset: float = 0.0,
                     jOffset: float = 0.0,
                     offsetIsFactor: bool = False,
                     imperf: float = 0.0,
                     imperfAngle: float = 0.0,
                     imperfPlane: np.ndarray = None):
    """Generate evenly-spaced coordinates for a 3D member, with optional rigid
    offset and sinusoidal imperfection calculation.

    Parameters
    ----------
    xi, yi, zi : float
        Coordinates of the i workpoint.

    xj, yj, zj : float
        Coordinates of the j workpoint.

    numElements : int
        Number of elements the member will consist of. numElements + 1 points
        are generated.

    iOffset : float, optional
        Distance from the i workpoint to the first coordinate. (default: 0.0)

    jOffset : float, optional
        Distance from the j workpoint to the last coordinate. (default: 0.0)

    offsetIsFactor : bool, optional
        If True, `iOffset` and `jOffset` specify offsets as a factor of the
        workpoint-to-workpoint length instead of absolute lengths. (default:
        False)

    imperf : float, optional
        Sinusoidal imperfection as a factor of the i-node to j-node length.
        (default: 0.0)

    imperfAngle : float, optional
        Angle of the imperfection from the xz plane defined by `imperfPlane`.
        (default: 0.0)

    imperfPlane : array_like, optional
        Vector that, along with the vector defined by the workpoint coordinates,
        defines the xz plane for the imperfection. This is usually the same
        vector that the OpenSees `geomTransf` command requires. If None, no
        imperfection is added to the returned coordinates. (default: None)

    Returns
    -------
    coords : np.ndarray
        2-d array with x-coordinates in the first row, y-coordinates in the
        second row, and z-coordinates in the third row. Can be unpacked as
        ``x, y, z = linspaceCoords3d(*args)``.
    """
    # Move origin to the i workpoint
    x = xj - xi
    y = yj - yi
    z = zj - zi

    # Calculate length and adjust for offsets
    L = np.sqrt(x**2 + y**2 + z**2)
    if offsetIsFactor:
        iOffset *= L
        jOffset *= L
    L = L - iOffset - jOffset

    # Location of points along the local x-axis
    xCoords = iOffset + np.linspace(0, L, numElements + 1)

    if imperfPlane is not None:
        # Calculate the imperfection in polar coordinates about the local x-axis
        imperf_r = imperf*L*np.sin(np.pi*(xCoords - iOffset)/L)
        zCoords = imperf_r*np.cos(imperfAngle)
        yCoords = imperf_r*np.sin(imperfAngle)

        # Calculate the local Cartesian system
        local_x = np.array([x, y, z])
        local_y = np.cross(imperfPlane, local_x)
        local_z = np.cross(local_x, local_y)

        # Unit vectors
        local_x = local_x/np.linalg.norm(local_x)
        local_y = local_y/np.linalg.norm(local_y)
        local_z = local_z/np.linalg.norm(local_z)

        # Rotate to global coordinates and translate back to original
        R = np.vstack((local_x, local_y, local_z)).T
        coords = R @ np.vstack((xCoords, yCoords, zCoords))
    else:
        # Without imperfection, things are simpler. Treat the local x-coords as
        # r in a spherical coordinate system, and back out cartesian coordinates
        # from there.
        rCoords = xCoords
        φ = np.arctan2(y, x)
        θ = np.arctan2(np.sqrt(x**2 + y**2), z)

        xCoords = rCoords*np.sin(θ)*np.cos(φ)
        yCoords = rCoords*np.sin(θ)*np.sin(φ)
        zCoords = rCoords*np.cos(θ)
        coords = np.vstack((xCoords, yCoords, zCoords))

    # Move origin back
    coords += np.array([xi, yi, zi]).reshape(-1, 1)
    return coords


#===============================================================================
# Output handling
#===============================================================================
def captureOutput(func):
    """Decorator to wrap a function, capturing stdout and stderr.

    Output is captured by `io.StringIO` objects that are attached to the
    function, and which can be accessed after calling the function:

    >>> @captureOutput
    ... def func():
    ...     pass
    ...
    >>> func()
    >>> func.stdout


        .. note::

        Functions that do not print to Python's standard output or standard
        error will not be successfully wrapped by this decorator. For example,
        a C++ library that prints directly to ``std::cerr`` will not be
        captured, as ``std::cerr`` bypasses Python's ``sys.stdout`` and
        ``sys.stderr``.

    Parameters
    ----------
    func
        Function to wrap.

    Examples
    --------

    Simple usage:

    >>> @captureOutput
    ... def sayHello():
    ...     print('hello!')
    ...
    >>> sayHello()  # No output
    >>> sayHello.stdout.getvalue()
    'hello!\\n'

    Both stdout and stderr are captured:

    >>> @captureOutput
    ... def sayWhoops():
    ...     print('hello!')
    ...     print('whoops!', file=sys.stderr)
    ...     return 0
    >>> sayWhoops()  # Nothing printed
    0
    >>> sayWhoops.stdout.getvalue()
    'hello!\\n'
    >>> sayWhoops.stderr.getvalue()
    'whoops!\\n'

    New `StringIO` objects are created each time the function is called:

    >>> sayHello()
    >>> sayHello.stdout
    <_io.StringIO at 0x7f18de15b550>
    >>> sayHello()
    >>> sayHello.stdout
    <_io.StringIO at 0x7f18f7968790>

    Captured output persists even if an error is thrown:

    >>> from openseestools import opensees as ops
    >>> @captureOutput
    ... def badOpenSeesCall():
    ...     ops.model()  # Not enough args
    ...
    >>> badOpenSeesCall()
    <Traceback>
    opensees.OpenSeesError: See stderr output
    >>> badOpenSeesCall.stderr.getvalue()
    'WARNING insufficient args: model -ndm ndm <-ndf ndf>\\n'
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.stdout = io.StringIO()
        wrapper.stderr = io.StringIO()
        with contextlib.redirect_stdout(wrapper.stdout):
            with contextlib.redirect_stderr(wrapper.stderr):
                return func(*args, **kwargs)

    return wrapper


#===============================================================================
# Fiber patches
#===============================================================================
def patchRect2d(matTag, nf, width, startHeight, endHeight):
    """Create a quadrilateral patch suitable for two-dimensional analyses.

    All fibers are placed on the z-axis.

    Parameters
    ----------
    matTag : int
        Tag of the uniaxial material to use.
    nf : int
        Number of fibers in the patch.
    width : float
        Width of the patch.
    startHeight : float
        Starting height of the patch.
    endHeight : float
        Ending height of the patch.
    """
    if startHeight >= endHeight:
        logger.warning('Creating fibers with a negative area')
    width = float(width)
    startHeight = float(startHeight)
    endHeight = float(endHeight)
    ops.patch('quad', int(matTag), int(nf), 1, startHeight, -width/2, endHeight,
              -width/2, endHeight, width/2, startHeight, width/2)


def patchHalfCircTube2d(matTag, nf, center, side, D, t):
    """Create a set of fibers to describe half a circular tube.

    Fibers are suitable for two-dimensional analyses since all fibers are placed
    on the Z-axis.

    Parameters
    ----------
    matTag : int
        Tag of the uniaxial material to use.
    nf : int
        Number of fibers along the height of the section.
    center : float
        Y-axis location of the center of the tube.
    side : {'top', 'bottom'}
        Side of the tube to create.
    D : float
        Diameter of the tube.
    t : float
        Thickness of the tube.

    Raises
    ------
    ValueError
        if `side` is not 'top' or 'bottom'
        if `D` is not a positive value
        if `t` is not a positive value
        if `t` is more than 0.5*`D`
    """
    if side.lower() not in ['top', 'bottom']:
        raise ValueError(
            "patchHalfCircTube2d: side should be either 'top' or 'bottom'")
    if D <= 0.0:
        raise ValueError('patchHalfCircTube2d: D should be a positive value')
    if t <= 0.0:
        raise ValueError('patchHalfCircTube2d: t should be a positive value')
    if t > 0.5*D:
        raise ValueError('patchHalfCircTube2d: t is too large relative to D')

    if side.lower() == 'top':
        sign = 1.0
    else:
        sign = -1.0

    ro = D/2
    ri = D/2 - t
    ystep = ro/nf

    for i in range(nf):
        yfar = ro - i*ystep
        ynear = max(ro - (i + 1)*ystep, 0.0)

        x = [0.0, 0.0]
        y = [
            centroidCircularSector(yfar, ro),
            centroidCircularSector(ynear, ro)
        ]
        A = [-areaCircularSector(yfar, ro), areaCircularSector(ynear, ro)]

        if yfar >= ri and ynear >= ri:
            pass
        elif yfar >= ri and ynear < ri:
            x.append(0.0)
            y.append(centroidCircularSector(ynear, ri))
            A.append(-areaCircularSector(ynear, ri))
        else:
            x.append(0.0)
            y.append(centroidCircularSector(yfar, ri))
            A.append(areaCircularSector(yfar, ri))
            x.append(0.0)
            y.append(centroidCircularSector(ynear, ri))
            A.append(-areaCircularSector(ynear, ri))

        _, centroid, area = nShapesCentroid(x, y, A)
        yf = center + sign*centroid
        logger.debug(f'Creating fiber at {yf:g} with area {area:g}')
        ops.fiber(yf, 0.0, area, matTag)


def fourFiberSectionGJ(secTag, matTag, area, Iy, Iz, GJ):
    """Create a fiber section with four fibers with desired section properties.

    Parameters
    ----------
    secTag
        Section tag. If None, defines just the fibers.
    matTag
        Uniaxial material to use.
    A : float
        Desired total cross-sectional area.
    Iy : float
        Desired moment of inertia about the y-axis of the section.
    Iz : float
        Desired moment of inertia about the z-axis of the section.
    GJ : float
        Desired torsional stiffness of the section. Not used if `secTag` is
        None.
    """
    if secTag is not None:
        ops.section('Fiber', int(secTag), '-GJ', float(GJ))
        fourFiberSectionGJ(None, matTag, area, Iy, Iz, GJ)
        return

    fiberA = float(0.25*area)
    fiberZ = float(np.sqrt(Iy/area))
    fiberY = float(np.sqrt(Iz/area))

    ops.fiber(+fiberY, +fiberZ, fiberA, int(matTag))
    ops.fiber(+fiberY, -fiberZ, fiberA, int(matTag))
    ops.fiber(-fiberY, +fiberZ, fiberA, int(matTag))
    ops.fiber(-fiberY, -fiberZ, fiberA, int(matTag))


def twoFiberSection(secTag, matTag, area, I):
    """Create a fiber section with two fibers with desired section properties.

    Parameters
    ----------
    secTag
        Section tag. If None, defines just the fibers.
    matTag
        Uniaxial material to use.
    A : float
        Desired total cross-sectional area.
    I : float
        Desired moment of inertia.
    """
    if secTag is not None:
        ops.section('Fiber', int(secTag))
        twoFiberSection(None, matTag, area, I)
        return

    fiberA = float(0.5*area)
    fiberY = float(np.sqrt(I/area))

    ops.fiber(+fiberY, 0.0, fiberA, int(matTag))
    ops.fiber(-fiberY, 0.0, fiberA, int(matTag))
