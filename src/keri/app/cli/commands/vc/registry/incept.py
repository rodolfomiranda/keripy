import argparse

from hio import help
from hio.base import doing

from keri.app import indirecting, habbing, grouping
from keri.app.cli.common import existing
from keri.vdr import credentialing

logger = help.ogler.getLogger()

parser = argparse.ArgumentParser(description='Initialize a prefix')
parser.set_defaults(handler=lambda args: registryIncept(args),
                    transferable=True)
parser.add_argument('--name', '-n', help='Human readable reference', required=True)
parser.add_argument('--registry-name', '-r', help='Human readable name for registry, defaults to name of Habitat',
                    default=None)
parser.add_argument("--no-backers", "-nb", help="do not allow setting up backers different from the ahcnoring KEL "
                                                "witnesses", default=True, action="store")
parser.add_argument('--backers', help='New set of backers different from the anchoring KEL witnesses.  Can '
                                      'appear multiple times', metavar="<prefix>", default=[], action="append",
                    required=False)
parser.add_argument("--establishment-only", "-eo", help="Only allow establishment events for the anchoring events of "
                                                        "this registry", default=False, action="store")
parser.add_argument('--base', '-b', help='additional optional prefix to file location of KERI keystore',
                    required=False, default="")
parser.add_argument('--alias', '-a', help='human readable alias for the new identifier prefix', required=True)
parser.add_argument('--passcode', '-p', help='22 character encryption passcode for keystore (is not saved)',
                    dest="bran", default=None)  # passcode => bran


def registryIncept(args):
    name = args.name
    alias = args.alias
    bran = args.bran
    base = args.base
    registryName = args.registry_name if args.registry_name is not None else alias
    estOnly = args.establishment_only
    noBackers = args.no_backers
    backers = args.backers

    if noBackers and backers:
        print("--no-backers and --backers can not both be provided")
        return -1

    icpDoer = RegistryInceptor(name=name, base=base, alias=alias, bran=bran, registryName=registryName,
                               estOnly=estOnly, noBackers=noBackers, baks=backers)

    doers = [icpDoer]
    return doers


class RegistryInceptor(doing.DoDoer):
    """

    """

    def __init__(self, name, base, alias, bran, registryName, **kwa):
        """


        """
        self.name = name
        self.alias = alias
        self.registryName = registryName
        self.hby = existing.setupHby(name=name, base=base, bran=bran)
        self.rgy = credentialing.Regery(hby=self.hby, name=name, base=base)
        self.hbyDoer = habbing.HaberyDoer(habery=self.hby)  # setup doer
        counselor = grouping.Counselor(hby=self.hby)

        mbx = indirecting.MailboxDirector(hby=self.hby, topics=["/receipt", "/multisig", "/replay"])
        self.icpr = credentialing.RegistryInceptDoer(hby=self.hby, rgy=self.rgy, counselor=counselor)
        doers = [self.hbyDoer, counselor, self.icpr, mbx]
        self.toRemove = list(doers)

        doers.extend([doing.doify(self.inceptDo)])
        super(RegistryInceptor, self).__init__(doers=doers, **kwa)

    def inceptDo(self, tymth, tock=0.0):
        """ Process incoming messages to incept a credential registry

        Parameters:
            tymth (function): injected function wrapper closure returned by .tymen() of
                Tymist instance. Calling tymth() returns associated Tymist .tyme.
            tock (float): injected initial tock value

        Returns:  doifiable Doist compatible generator method
        """
        # enter context
        self.wind(tymth)
        self.tock = tock
        _ = (yield self.tock)

        hab = self.hby.habByName(self.alias)
        msg = dict(name=self.registryName, pre=hab.pre)
        self.icpr.msgs.append(msg)

        regk = None
        while not regk:
            while self.icpr.cues:
                cue = self.icpr.cues.popleft()
                if cue["kin"] == "finished":
                    regk = cue["regk"]
                    break
                yield self.tock
            yield self.tock

        print("Regsitry:  {}({}) \n\tcreated for Identifier Prefix:  {}".format(self.registryName, regk, hab.pre))

        self.remove(self.toRemove)
