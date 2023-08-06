from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.objects import NetworkObject


__all__ = ['NetworkObject']


class NetworkObject(NetworkObject):
    """A customised `NetworkArtist` for 3GS `Network`-based data structures."""

    @property
    def diagram(self):
        """The diagram associated with the object."""
        return self.network

    @diagram.setter
    def diagram(self, diagram):
        self.network = diagram
