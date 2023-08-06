"""netcdf provides methods for dealing with netcdf files in drama."""
import numpy as np


class NETCDFHandler(object):
    """Child class to ease netCDF file handling.

    Notes
    -----
    * Class variable __file__ contains the netCDF file object
    * __file__ needs to be properly initialized by parent class
    * Complex types are supported in the following way:
        - Define the variable real and imaginary parts with
          suffixes _r, _i respectively, i.e. test_r, test_i
        - Use get/set methods appending '*' to variable name,
          i.e. get('test*'), set('test*', complex_array)
    """

    def close(self):
        """Close file."""
        self.__file__.close()

    def get(self, name):
        """Get variable content.

        Parameters
        ----------
        name : str
            Variable name

        Returns
        -------
        the content of the netcdf under the variable name
        """
        if name[-1] == "*":
            content = np.empty(
                self.__file__.variables[name[:-1] + "_r"].shape, complex
            )
            content.real = self.__file__.variables[name[:-1] + "_r"][:]
            content.imag = self.__file__.variables[name[:-1] + "_i"][:]
        else:
            content = self.__file__.variables[name][:]

        # return content[0] if content.size == 1 else content
        return content

    def set(self, name, value):
        """Set variable content

        Parameters
        ----------
        name : str
            Variable name
        value : any type of value supported by netcdf
            Variable content
        """
        if name[-1] == "*":
            self.__file__.variables[name[:-1] + "_r"][:] = value.real
            self.__file__.variables[name[:-1] + "_i"][:] = value.imag
        else:
            self.__file__.variables[name][:] = value
