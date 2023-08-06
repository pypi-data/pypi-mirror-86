import numpy as np

_possible_electrode_shapes = ['circle', 'square', 'rect']

class Probe:
    """
    Class to handle the geometry of one probe.
    
    Handle mainly electrode position.
    
    Can be 2D or 3D.
    
    Can handle also optionally the shape of eletrode and the shape of the probe.
    
    
    """
    def __init__(self, ndim=2, si_units='um'):
        """
        
        Parameters
        ----------
        ndim: 2 or 3
            handle 2D or 3D probe
        
        si_units: 'um', 'mm', 'm'
        
        """
        self.ndim = ndim
        self.si_units = si_units
        
        # electrode position and shape : handle with arrays
        self.electrode_positions = None
        self.electrode_shapes = None
        self.electrode_shape_params = None
        
        # shape of the probe
        self.probe_shape = None
        
        
    
    def get_electrode_count(self):
        """
        Return how many electrodes on the probe.
        """
        assert self.electrode_positions is not None
        return len(self.electrode_positions)
    
    def set_electrodes(self, positions=None, shapes='circle', shape_params={'radius': 10}):
        """
        Parameters
        ----------
        positions : array of posisitions
        
        shapes: scalar or array in 'circle'/'square'/'rect'
            Shape for each electrodes.
        
        shape_params dict or list of dict
            Contain kargs for shapes ("radius" for circle, "width" for sqaure, "width/height" for rect)
        """
        assert positions is not None
        
        positions = np.array(positions)
        if positions.shape[1] != self.ndim:
            raise ValueErrorr('posistions.shape[1] and ndim do not match!')
        
        self.electrode_positions = positions
        n = positions.shape[0]
        
        # shape
        if isinstance(shapes, str):
            shapes = [shapes] * n
        shapes = np.array(shapes)
        if not np.all(np.in1d(shapes, _possible_electrode_shapes)):
            raise ValueError(f'Electrodes shape must be in {_possible_electrode_shapes}')
        if shapes.shape[0] !=n:
            raise ValueError(f'Electrodes shape must have same length as posistions')
        self.electrode_shapes = np.array(shapes)
        
        # shape params
        if isinstance(shape_params, dict):
            shape_params = [shape_params] * n
        self.electrode_shape_params = np.array(shape_params)
    
    def copy(self):
        """
        Copy to another Probe instance.
        """
        other = Probe()
        other.set_electrodes(
                    positions=self.electrode_positions.copy(),
                    shapes=self.electrode_shapes.copy(),
                    shape_params=self.electrode_shape_params.copy())
        return other

    def to_3d(self, plane='xy'):
        """
        Transform 2d probe to 3d probe.

        Parameters
        ----------
        plane: 'xy', 'yz' ', xz'
        """
        assert self.ndim ==2
        
        pos = self.electrode_positions
        positions = np.zeros((pos.shape[0], 3))
        
        if plane == 'xy':
            positions[:, 0] = pos[:, 0]
            positions[:, 1] = pos[:, 1]
        elif plane == 'yz':
            positions[:, 1] = pos[:, 0]
            positions[:, 2] = pos[:, 1]
        elif plane == 'xz':
            positions[:, 0] = pos[:, 0]
            positions[:, 2] = pos[:, 1]
        else:
            raise ValueError('Bad plane')
        
        # probe3d = Probe(ndim=3, si_units=self.si_units)
        probe3d.set_electrodes(
                    positions=positions,
                    shapes=self.electrode_shapes.copy(),
                    shape_params=self.electrode_shape_params.copy())
        # return probe3d
    
    def rotate(self, axis, theta, origin):
        """
        Rorate the probe the specified axis

        Parameters
        ----------
        axis
        
        theta
        
        origin
        """
        raise NotImplementedError
    
    def move(self, direction):
        """
        Move the probe toward a direction.
        
        Parameters
        ----------
        direction
        """
        raise NotImplementedError
    
    
    
    


