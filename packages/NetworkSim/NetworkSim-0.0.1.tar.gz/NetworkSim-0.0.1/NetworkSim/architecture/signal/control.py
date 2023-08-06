import pandas as pd


class ControlSignal:
    """
    Constructor for control signals.

    The user defines the bit lengths of both the Source/Destination ID and the Control bits

    Parameters
    ----------
    id_length : int, optional
        The bit length of the source and destination IDs.
        Default is ``7`` for 100 nodes.
    control_length : int, optional
        The bit length of the control bits.
        Default is ``2``.

    Attributes
    ----------
    control_info : dictionary
        A dictionary containing information about the control bits.
    """

    def __init__(
            self,
            id_length=7,
            control_length=2
    ):
        self.id_length = id_length
        self.control_length = control_length
        # Define control bits dictionary
        self.control_info = {
            0: 'New Data',
            1: 'Removed Data'
        }

    def get_code(self, code):
        """
        Obtain information about control code.

        Parameters
        ----------
        code : int
            Control code in decimal.

        Returns
        -------
        control_info : str
            Control code corresponding representation.
        """
        return self.control_info[code]

    def get_info(self):
        """
        Obtain information about the control signals.

        Returns
        -------
        info : pandas DataFrame
            A pandas DataFrame containing control signal's decimal code, binary code, \
            and respective representations, containing the columns:

            - `Decimal`
            - `Binary`
            - `Representation`
        """
        info = {
            'Decimal': list(self.control_info.keys()),
            'Binary': [bin(n)[2:].zfill(self.control_length) for n in list(self.control_info.keys())],
            'Representation': list(self.control_info.values())
        }
        return pd.DataFrame.from_dict(info)

    def set_info(self, new_info):
        """
        Set information about the control signals.

        Parameters
        ----------
        new_info : dict
            New information of the control signals.
        """
        if not isinstance(new_info, dict):
            raise ValueError('Control information must be in the format of a dictionary.')
        self.control_info = new_info

    def generate_packet(self, source, destination, control):
        """
        Control packet generation.

        Parameters
        ----------
        source : int
            Source node ID.
        destination : int
            Destination node ID.
        control : int
            Control code in decimal.

        Returns
        -------
        control_packet : str
            The control packet string in binary.
        """
        # Check input types
        if not isinstance(source, int) or not isinstance(destination, int) or not isinstance(control, int):
            raise ValueError('All inputs must be integers.')
        # Generate all three parts of the control packet
        packet_source = bin(source)[2:].zfill(self.id_length)
        packet_destination = bin(destination)[2:].zfill(self.id_length)
        packet_control = bin(control)[2:].zfill(self.control_length)
        return packet_source + packet_destination + packet_control
