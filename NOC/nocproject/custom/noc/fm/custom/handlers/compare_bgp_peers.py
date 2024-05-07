


# ---------------------------------------------------------------------
# compare_bgp_peers handlers
# ---------------------------------------------------------------------
# Copyright (C) 2007-2020 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import logging
import os


# NOC modules
from noc.sa.models.managedobject import ManagedObject
from noc.peer.models.peer import Peer
from noc.services.correlator.service import CorrelatorService

"""

log_directory = '/var/log/noc/'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_file = os.path.join(log_directory, 'bgp_peers.log')
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
"""

def peers_bgp(event):
    """
    Set oper status to down
    """
    peer = Peer.objects.filter(
        peer_group_id=1, remote_ip=f"({event.vars['peer']}/30)"
    ).first()
    print(peer)
    if peer:
        event.to_dispose()
    else:
        event.do_not_dispose()

#file_handler.close()





