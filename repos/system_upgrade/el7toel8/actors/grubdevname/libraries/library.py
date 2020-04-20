import os

from leapp.libraries.stdlib import run, api, CalledProcessError
from leapp.exceptions import StopActorExecution
from leapp.models import GrubDevice


def has_grub(blk_dev):
    """
    Check whether GRUB is present on block device
    """
    try:
        with os.open(blk_dev, os.O_RDONLY) as blk:
            mbr = os.read(blk, 512)
    except:
        api.current_logger().warning(
            'Could not read first sector of {} in order to identify the bootloader'.format(blk_dev)
        )
        raise StopActorExecution()
    return b'GRUB' in mbr


def blk_dev_from_partition(partition):
    """
    Find parent device of /boot partition
    """
    try:
        result = run(['lsblk', '-spnlo', 'name', partition])
    except CalledProcessError:
        api.current_logger().warning(
            'Could not get parent device of {} partition'.format(partition)
        )
        raise StopActorExecution()
    # lsblk "-s" option prints dependencies in inverse order, so the parent device will always
    # be the last or the only device.
    # Command result example:
    # 'result', {'signal': 0, 'pid': 3872, 'exit_code': 0, 'stderr': u'', 'stdout': u'/dev/vda1\n/dev/vda\n'}
    return result['stdout'].strip().split()[-1]


def get_boot_partition():
    """
    Get /boot partition
    """
    try:
        # call grub2-probe to identify /boot partition
        result = run(['grub2-probe', '--target=device', '/boot'])
    except CalledProcessError:
        api.current_logger().warning(
            'Could not get name of underlying /boot partition'
        )
        raise StopActorExecution()
    return result['stdout'].strip()


def get_grub_device():
    """
    Get block device where GRUB is located. We assume GRUB is on the same device
    as /boot partition is.

    """
    grub_dev = os.getenv('LEAPP_GRUB_DEVICE', None)
    if grub_dev:
        api.produce(GrubDevice(grub_device=grub_dev))
        return
    boot_partition = get_boot_partition()
    grub_dev = blk_dev_from_partition(boot_partition)
    if grub_dev:
        if has_grub(grub_dev):
            api.produce(GrubDevice(grub_device=grub_dev))
