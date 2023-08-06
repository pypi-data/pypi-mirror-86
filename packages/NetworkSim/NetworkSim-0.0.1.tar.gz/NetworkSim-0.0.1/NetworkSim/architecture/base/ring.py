__all__ = ["Ring"]
__author__ = ["Hongyi Yang"]

import numpy as np
import pandas as pd


class Ring:
    """
    Ring class to store packets on both control and data rings.
    Packets can be added or removed from the ring.
    Time of addition of the packet is recorded to track packet location.

    Parameters
    ----------
    model : Model
        The network model used. Default is ``Model()``.
    time_unit : str
        The time unit used for the simulation, chosen from the following:

        - 'ns'
        - 's'

        Default is ``'ns'``

    Attributes
    ----------
    ring_id : int
        The ID of the ring. Default is ``None``.
    nodes_location : array
        Array of locations of the nodes on the ring, in meters.
    packets : list
        List of packets present on the ring, containing:

        - `raw_packet` : str
            The raw packet string.
        - `generation_timestamp` : float
            Time when the packet was generated and stored into the RAM.
        - `transmission_timestamp` : float
            Time when the packet was added onto the ring.
        - `packet_entry_point` : float
            The location (in meters) where the packet was added.
        - `entry_node_id` : int
            The ID of the node where the packet was added.
        - `destination_node_id` : int
            The ID of the destination of the packet.
    packet_record_df : pandas DataFrame
        A DataFrame containing the information on all packet transmission on the ring, including the columns:

        - `Generation Timestamp` : float
            The timestamp when the packet is generated and stored in the RAM.
        - `Transmission Timestamp` : float
            The timestamp when the packet is added onto the ring by the transmitter.
    """

    def __init__(
            self,
            model,
            ring_id=None,
            time_unit='ns'
    ):
        self.model = model
        self.ring_id = ring_id
        self.nodes_location = self.get_nodes_location()
        self.packets = []
        self.packet_count = 0
        data = []
        self.packet_record_df = pd.DataFrame(data, columns=[
            'Generation Timestamp',
            'Transmission Timestamp',
            'Reception Timestamp',
            'Raw Packet',
            'Source Node',
            'Destination Node',
            'Status',
            'Total Packet Count'
        ])
        self.time_unit = time_unit

    def get_nodes_location(self):
        """
        Get locations of all nodes in the ring.

        Returns
        -------
        locations : numpy array
            An array of node locations.
        """
        locations = np.linspace(start=0,
                                stop=self.model.network.length,
                                num=self.model.network.num_nodes + 1)
        return locations[:-1]

    def add_packet(self, node_id, destination_id, packet, generation_timestamp, transmission_timestamp):
        """
        Packet addition to the ring.
        The packet added will be in the format `[raw_packet, timestamp, node_id]`.

        Parameters
        ----------
        node_id : int
            The ID of the node at which the packet is added.
        destination_id : int
            The ID of the destination node of the packet.
        packet : str
            The packet string added onto the ring.
        generation_timestamp : float
            The timestamp when the packet is generated.
        transmission_timestamp : float
            The timestamp when the packet is added.
        """
        # Check input types
        if not isinstance(node_id, int):
            raise ValueError('Input node_id must be an integer.')
        if not isinstance(packet, str):
            raise ValueError('Input packet must be str')

        # Add packet to the ring
        self.packets.append([
            packet,
            generation_timestamp,
            transmission_timestamp,
            self.nodes_location[node_id],
            node_id,
            destination_id
        ])
        self.packet_count += 1
        self.packet_record_df = self.packet_record_df.append({
            'Generation Timestamp': generation_timestamp,
            'Transmission Timestamp': transmission_timestamp,
            'Raw Packet': packet,
            'Source Node': node_id,
            'Destination Node': destination_id,
            'Status': 'added',
            'Total Packet Count': self.packet_count
        }, ignore_index=True)

    def remove_packet(self, node_id, packet, reception_timestamp):
        """
        Packet removal from the ring.

        Parameters
        ----------
        node_id : int
            The ID of the node where the packet is removed.
        packet : packet
            The packet to be removed from the ring, containing:

            - `raw_packet`
            - `generation_timestamp`
            - `transmission_timestamp`
            - `packet_entry_point`
            - `entry_node_id`
            - `destination_node_id`

        reception_timestamp : float
            The timestamp at which the packet is removed.
        """
        self.packets.remove(packet)
        self.packet_count -= 1
        self.packet_record_df = self.packet_record_df.append({
            'Generation Timestamp': packet[1],
            'Transmission Timestamp': packet[2],
            'Reception Timestamp': reception_timestamp,
            'Raw Packet': packet[0],
            'Source Node': packet[4],
            'Destination Node': node_id,
            'Status': 'removed',
            'Total Packet Count': self.packet_count
        }, ignore_index=True)

    def check_packet(self, current_time, node_id):
        """
        Packet existence check.

        Parameters
        ----------
        current_time : float
            Current time when the packet is checked.
        node_id : int
            Id of the node at which the check is performed.

        Returns
        -------
        existence : bool
            The existence of the packet. ``True`` when a packet exists.
        packet : packet
            The packet information, containing:

            - `raw_packet`
            - `generation_timestamp`
            - `transmission_timestamp`
            - `packet_entry_point`
            - `entry_node_id`
            - `destination_node_id`
        """
        # Check input
        if not isinstance(node_id, int):
            raise ValueError('Input node_id must be an integer.')
        # Check presence of packet based on current time
        for packet in self.packets:
            # Compare current location of packet with node location with time in ns
            if self.time_unit == 'ns':
                new_location = packet[3] + (current_time - packet[2]) * self.model.constants.get('speed') * 1e-9
            if self.time_unit == 's':
                new_location = packet[3] + (current_time - packet[2]) * self.model.constants.get('speed')
            new_location_on_ring = new_location % self.model.network.length
            if np.isclose(new_location_on_ring, self.nodes_location[node_id], atol=1e-2):
                return True, packet
        # No packet present
        return False, None
