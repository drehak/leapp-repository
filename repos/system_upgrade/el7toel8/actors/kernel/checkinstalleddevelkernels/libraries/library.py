from leapp import reporting
from leapp.libraries.stdlib import api
from leapp.models import InstalledRedHatSignedRPM


def get_kernel_rpm_release(rpm):
    """
    Get the release of a kernel RPM as an integer.

    :param rpm: An instance of an RPM derived model.
    """
    return int(rpm.release.split('.')[0])


def get_kernel_devel_rpms():
    """
    Get all installed kernel-devel packages ordered by release number (ascending).
    """
    rpms = next(api.consume(InstalledRedHatSignedRPM), InstalledRedHatSignedRPM())
    return sorted([pkg for pkg in rpms.items if pkg.name == 'kernel-devel'], key=get_kernel_rpm_release)


def process():
    pkgs = get_kernel_devel_rpms()
    if len(pkgs) > 1:
        title = 'Multiple devel kernels installed'
        summary = ('DNF cannot produce a valid upgrade transaction when'
                   ' multiple kernel-devel packages are installed.')
        hint = ('Remove all but one kernel-devel packages before running Leapp again.')
        commands = ([['yum', '-y', 'remove', '{n}-{v}.{r}'.format(
            n=pkg.name, v=pkg.version, r=pkg.release)] for pkg in pkgs[:-1]])
        reporting.create_report([
            reporting.Title(title),
            reporting.Summary(summary),
            reporting.Severity(reporting.Severity.HIGH),
            reporting.Tags([reporting.Tags.KERNEL]),
            reporting.Flags([reporting.Flags.INHIBITOR]),
            reporting.Remediation(hint=hint, commands=commands),
            reporting.RelatedResource('package', 'kernel')
        ])
