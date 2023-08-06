import logging

log_format = ('[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s')

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    filename=("embox_electrostatic.log")
)

logger = logging.getLogger("electrostatic_logger")

