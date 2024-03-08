# -*- encoding: utf-8 -*-
"""
tests.app.apping module

"""
import pytest

import os
import shutil

from hio.base import doing

from keri import kering
from keri import help
from keri.app import habbing, keeping, configing
from keri.db import basing
from keri.core import coring, eventing, parsing
from keri.help import helping


def test_habery():
    """
    Test Habery class
    """
    # test default
    default_salt = coring.Salter(raw=b'0123456789abcdef').qb64
    hby = habbing.Habery(temp=True, salt=default_salt)
    assert hby.name == "test"
    assert hby.base == ""
    assert hby.temp
    assert hby.inited
    assert hby.habs == {}

    assert hby.db.name == "test" == hby.name
    assert hby.db.base == "" == hby.base
    assert not hby.db.filed
    assert hby.db.path.endswith("/keri/db/test")
    assert hby.db.opened

    assert hby.ks.name == "test" == hby.name
    assert hby.ks.base == "" == hby.base
    assert not hby.ks.filed
    assert hby.ks.path.endswith("/keri/ks/test")
    assert hby.ks.opened

    assert hby.cf.name == "test" == hby.name
    assert hby.cf.base == "" == hby.base
    assert hby.cf.filed
    assert hby.cf.path.endswith("/keri/cf/test.json")
    assert hby.cf.opened
    assert not hby.cf.file.closed

    assert hby.mgr.seed == ""
    assert hby.mgr.aeid == ""
    assert hby.mgr.salt == default_salt
    assert hby.mgr.pidx == 1
    assert hby.mgr.algo == keeping.Algos.salty
    assert hby.mgr.tier == coring.Tiers.low

    hby.cf.close(clear=True)
    hby.db.close(clear=True)
    hby.ks.close(clear=True)

    assert not os.path.exists(hby.cf.path)
    assert not os.path.exists(hby.db.path)
    assert not os.path.exists(hby.ks.path)

    # test bran to seed
    bran = "MyPasscodeARealSecret"
    assert len(bran) == 21
    # these are the ones generated by Manager for the given bran
    # bran = coring.MtrDex.Salt_128 + 'A' + bran[:21]  # qb64 salt for seed
    # signer = coring.Salter(qb64=bran).signer(transferable=False, tier=tier, temp=temp)
    # seed = signer.qb64
    # aeid = signer.verfer.qb64  # lest it remove encryption
    seed4bran = 'ALQVu9AjGW3JrIzX0UHm2awGCbDXcsLzy-vAE649Fz1j'
    aeid4seed = 'BHRYV_5a1AlibCrXFG_KDD9rC6aXx9cb0sR968NL80VI'

    hby = habbing.Habery(bran=bran, temp=True, salt=default_salt)
    assert hby.name == "test"
    assert hby.base == ""
    assert hby.temp
    assert hby.inited
    assert hby.habs == {}

    assert hby.mgr.seed == seed4bran
    assert hby.mgr.aeid == aeid4seed
    assert hby.mgr.salt == default_salt
    assert hby.mgr.pidx == 1
    assert hby.mgr.algo == keeping.Algos.salty
    assert hby.mgr.tier == coring.Tiers.low

    assert hby.rtr.routes
    assert hby.rvy.rtr == hby.rtr
    assert hby.kvy.rvy == hby.rvy
    assert hby.psr.kvy == hby.kvy
    assert hby.psr.rvy == hby.rvy

    hby.cf.close(clear=True)
    hby.db.close(clear=True)
    hby.ks.close(clear=True)

    assert not os.path.exists(hby.cf.path)
    assert not os.path.exists(hby.db.path)
    assert not os.path.exists(hby.ks.path)

    # test pre-create of injected resources
    base = "keep"
    name = "main"
    bran = "MyPasscodeARealSecret"
    temp = True

    # setup databases  for dependency injection and config file
    ks = keeping.Keeper(name=base, temp=temp)  # not opened by default, doer opens
    ksDoer = keeping.KeeperDoer(keeper=ks)  # doer do reopens if not opened and closes
    db = basing.Baser(name=base, temp=temp)  # not opened by default, doer opens
    dbDoer = basing.BaserDoer(baser=db)  # doer do reopens if not opened and closes
    cf = configing.Configer(name=name, base=base, temp=temp)
    cfDoer = configing.ConfigerDoer(configer=cf)
    conf = cf.get()
    if not conf:  # setup config file
        curls = ["ftp://localhost:5620/"]
        iurls = [f"ftp://localhost:5621/?role={kering.Roles.peer}&name=Bob"]
        conf = dict(dt=help.nowIso8601(), curls=curls, iurls=iurls)
        cf.put(conf)

    # setup habery
    hby = habbing.Habery(name=name, base=base, ks=ks, db=db, cf=cf, temp=temp,
                         bran=bran, salt=default_salt)
    hbyDoer = habbing.HaberyDoer(habery=hby)  # setup doer

    assert hby.name == "main"
    assert hby.base == "keep"
    assert hby.temp
    assert not hby.inited
    assert hby.mgr is None

    # need to run doers to open databases so can finish init
    doers = [ksDoer, dbDoer, cfDoer, hbyDoer]

    # run components
    tock = 0.03125
    limit = 1.0
    doist = doing.Doist(limit=limit, tock=tock, real=True)

    # doist.do(doers=doers)
    deeds = doist.enter(doers=doers)
    doist.recur(deeds=deeds)

    assert hby.inited
    assert hby.habs == {}
    assert hby.mgr is not None
    assert hby.mgr.seed == seed4bran
    assert hby.mgr.aeid == aeid4seed
    assert hby.mgr.salt == default_salt
    assert hby.mgr.pidx == 1
    assert hby.mgr.algo == keeping.Algos.salty
    assert hby.mgr.tier == coring.Tiers.low

    assert hby.rtr.routes
    assert hby.rvy.rtr == hby.rtr
    assert hby.kvy.rvy == hby.rvy
    assert hby.psr.kvy == hby.kvy
    assert hby.psr.rvy == hby.rvy

    doist.exit(deeds=deeds)

    assert not cf.opened
    assert not db.opened
    assert not ks.opened

    assert not os.path.exists(cf.path)
    assert not os.path.exists(db.path)
    assert not os.path.exists(ks.path)

    # test pre-create using habery itself
    base = "keep"
    name = "main"
    bran = "MyPasscodeARealSecret"
    temp = True

    # setup habery with resources
    hby = habbing.Habery(name=name, base=base, temp=temp, bran=bran, free=True, salt=default_salt)
    hbyDoer = habbing.HaberyDoer(habery=hby)  # setup doer

    conf = hby.cf.get()
    if not conf:  # setup config file
        curls = ["ftp://localhost:5620/"]
        iurls = [f"ftp://localhost:5621/?role={kering.Roles.peer}&name=Bob"]
        conf = dict(dt=help.nowIso8601(), curls=curls, iurls=iurls)
        hby.cf.put(conf)

    assert hby.name == "main"
    assert hby.base == "keep"
    assert hby.temp
    assert hby.inited
    assert hby.mgr is not None

    # habery doer to free resources on exit
    doers = [hbyDoer]

    # run components
    tock = 0.03125
    limit = 1.0
    doist = doing.Doist(limit=limit, tock=tock, real=True)

    # doist.do(doers=doers)
    deeds = doist.enter(doers=doers)
    doist.recur(deeds=deeds)

    assert hby.inited
    assert hby.habs == {}
    assert hby.mgr is not None
    assert hby.mgr.seed == seed4bran
    assert hby.mgr.aeid == aeid4seed
    assert hby.mgr.salt == default_salt
    assert hby.mgr.pidx == 1
    assert hby.mgr.algo == keeping.Algos.salty
    assert hby.mgr.tier == coring.Tiers.low

    assert hby.rtr.routes
    assert hby.rvy.rtr == hby.rtr
    assert hby.kvy.rvy == hby.rvy
    assert hby.psr.kvy == hby.kvy
    assert hby.psr.rvy == hby.rvy

    doist.exit(deeds=deeds)

    assert not hby.cf.opened
    assert not hby.db.opened
    assert not hby.ks.opened

    assert not os.path.exists(hby.cf.path)
    assert not os.path.exists(hby.db.path)
    assert not os.path.exists(hby.ks.path)

    with habbing.openHby(salt=coring.Salter(raw=b'0123456789abcdef').qb64) as hby:
        assert hby.name == "test"
        assert hby.base == ""
        assert hby.temp
        assert hby.inited

        assert hby.db.name == "test" == hby.name
        assert hby.db.base == "" == hby.base
        assert not hby.db.filed
        assert hby.db.path.endswith("/keri/db/test")
        assert hby.db.opened

        assert hby.ks.name == "test" == hby.name
        assert hby.ks.base == "" == hby.base
        assert not hby.ks.filed
        assert hby.ks.path.endswith("/keri/ks/test")
        assert hby.ks.opened

        assert hby.cf.name == "test" == hby.name
        assert hby.cf.base == "" == hby.base
        assert hby.cf.filed
        assert hby.cf.path.endswith("/keri/cf/test.json")
        assert hby.cf.opened
        assert not hby.cf.file.closed

        assert hby.mgr.seed == ""
        assert hby.mgr.aeid == ""
        assert hby.mgr.salt == default_salt
        assert hby.mgr.pidx == 1
        assert hby.mgr.algo == keeping.Algos.salty
        assert hby.mgr.tier == coring.Tiers.low

        assert hby.rtr.routes
        assert hby.rvy.rtr == hby.rtr
        assert hby.kvy.rvy == hby.rvy
        assert hby.psr.kvy == hby.kvy
        assert hby.psr.rvy == hby.rvy

    assert not hby.cf.opened
    assert not hby.db.opened
    assert not hby.ks.opened

    assert not os.path.exists(hby.cf.path)
    assert not os.path.exists(hby.db.path)
    assert not os.path.exists(hby.ks.path)

    bran = "MyPasscodeARealSecret"
    with habbing.openHby(bran=bran, salt=coring.Salter(raw=b'0123456789abcdef').qb64) as hby:
        assert hby.name == "test"
        assert hby.base == ""
        assert hby.temp
        assert hby.inited
        assert hby.habs == {}

        assert hby.db.name == "test" == hby.name
        assert hby.db.base == "" == hby.base
        assert not hby.db.filed
        assert hby.db.path.endswith("/keri/db/test")
        assert hby.db.opened

        assert hby.ks.name == "test" == hby.name
        assert hby.ks.base == "" == hby.base
        assert not hby.ks.filed
        assert hby.ks.path.endswith("/keri/ks/test")
        assert hby.ks.opened

        assert hby.cf.name == "test" == hby.name
        assert hby.cf.base == "" == hby.base
        assert hby.cf.filed
        assert hby.cf.path.endswith("/keri/cf/test.json")
        assert hby.cf.opened
        assert not hby.cf.file.closed

        # test bran to seed
        assert hby.mgr.seed == seed4bran
        assert hby.mgr.aeid == aeid4seed
        assert hby.mgr.salt == default_salt
        assert hby.mgr.pidx == 1
        assert hby.mgr.algo == keeping.Algos.salty
        assert hby.mgr.tier == coring.Tiers.low

        assert hby.rtr.routes
        assert hby.rvy.rtr == hby.rtr
        assert hby.kvy.rvy == hby.rvy
        assert hby.psr.kvy == hby.kvy
        assert hby.psr.rvy == hby.rvy

    assert not hby.cf.opened
    assert not hby.db.opened
    assert not hby.ks.opened

    assert not os.path.exists(hby.cf.path)
    assert not os.path.exists(hby.db.path)
    assert not os.path.exists(hby.ks.path)

    """End Test"""


def test_make_load_hab_with_habery():
    """
    Test creation methods for Hab instances with Habery
    """
    with pytest.raises(TypeError):  # missing required dependencies
        _ = habbing.Hab()  # defaults

    name = "sue"
    suePre = 'ELF1S0jZkyQx8YtHaPLu-qyFmrkcykAiEW8twS-KPSO1'  # with temp=True

    with habbing.openHby(salt=coring.Salter(raw=b'0123456789abcdef').qb64) as hby:  # default is temp=True on openHab
        hab = hby.makeHab(name=name)
        assert isinstance(hab, habbing.Hab)
        assert hab.pre in hby.habs
        assert id(hby.habByName(hab.name)) == id(hab)

        assert hab.name == name
        assert hab.pre == suePre
        assert hab.temp
        assert hab.accepted
        assert hab.inited

        assert hab.pre in hby.kevers
        assert hab.pre in hby.prefixes

        hab.db = hby.db  # injected
        hab.ks = hby.ks  # injected
        hab.cf = hby.cf  # injected
        hab.mgr = hby.mgr  # injected
        hab.rtr = hby.rtr  # injected
        hab.rvy = hby.rvy  # injected
        hab.kvy = hby.kvy  # injected
        hab.psr = hby.psr  # injected

    assert not hby.cf.opened
    assert not hby.db.opened
    assert not hby.ks.opened

    assert not os.path.exists(hby.cf.path)
    assert not os.path.exists(hby.db.path)
    assert not os.path.exists(hby.ks.path)

    # create not temp and then reload from not temp
    if os.path.exists('/usr/local/var/keri/cf/hold/test.json'):
        os.remove('/usr/local/var/keri/cf/hold/test.json')
    if os.path.exists('/usr/local/var/keri/db/hold/test'):
        shutil.rmtree('/usr/local/var/keri/db/hold/test')
    if os.path.exists('/usr/local/var/keri/ks/hold/test'):
        shutil.rmtree('/usr/local/var/keri/ks/hold/test')

    base = "hold"
    suePre = 'EAxe215BJ4Iy9r0mfoMEGVmHW8A4Avk3RYBC1A1_DZam'  # with temp=False
    bobPre = 'ENya5E5pvc6MVCe75huDK0QQhE4_64J55vCn4aKdXhR9'  # with temp=False

    with habbing.openHby(base=base, temp=False, salt=coring.Salter(raw=b'0123456789abcdef').qb64) as hby:  # default is temp=True
        assert hby.cf.path.endswith("keri/cf/hold/test.json")
        assert hby.db.path.endswith("keri/db/hold/test")
        assert hby.ks.path.endswith('keri/ks/hold/test')

        sueHab = hby.makeHab(name='Sue')
        assert isinstance(sueHab, habbing.Hab)
        assert sueHab.pre in hby.habs
        assert id(hby.habByName(sueHab.name)) == id(sueHab)

        assert sueHab.name == "Sue"
        assert sueHab.pre == suePre
        assert not sueHab.temp
        assert sueHab.accepted
        assert sueHab.inited
        assert sueHab.pre in hby.kevers
        assert sueHab.pre in hby.prefixes

        bobHab = hby.makeHab(name='Bob')
        assert isinstance(bobHab, habbing.Hab)
        assert bobHab.pre in hby.habs
        assert id(hby.habByName(bobHab.name)) == id(bobHab)

        assert bobHab.name == "Bob"
        assert bobHab.pre == bobPre
        assert not bobHab.temp
        assert bobHab.accepted
        assert bobHab.inited
        assert bobHab.pre in hby.kevers
        assert bobHab.pre in hby.prefixes

        assert len(hby.habs) == 2

    assert not hby.cf.opened
    assert not hby.db.opened
    assert not hby.ks.opened

    assert os.path.exists(hby.cf.path)
    assert os.path.exists(hby.db.path)
    assert os.path.exists(hby.ks.path)

    # test load from database
    base = "hold"
    with habbing.openHby(base=base, temp=False) as hby:  # default is temp=True
        assert hby.cf.path.endswith("keri/cf/hold/test.json")
        assert hby.db.path.endswith("keri/db/hold/test")
        assert hby.ks.path.endswith('keri/ks/hold/test')

        assert hby.inited
        assert len(hby.habs) == 2

        assert suePre in hby.kevers
        assert suePre in hby.prefixes
        assert suePre in hby.habs
        sueHab = hby.habByName("Sue")
        assert sueHab.name == "Sue"
        assert sueHab.pre == suePre
        assert sueHab.accepted
        assert sueHab.inited

        assert bobPre in hby.kevers
        assert bobPre in hby.prefixes
        assert bobPre in hby.habs
        bobHab = hby.habByName("Bob")
        assert bobHab.name == "Bob"
        assert bobHab.pre == bobPre
        assert bobHab.accepted
        assert bobHab.inited

    hby.close(clear=True)
    hby.cf.close(clear=True)
    assert not os.path.exists(hby.cf.path)
    assert not os.path.exists(hby.db.path)
    assert not os.path.exists(hby.ks.path)

    """End Test"""


def test_hab_rotate_with_witness():
    """
    Reload from disk and rotate hab with witness
    """

    if os.path.exists('/usr/local/var/keri/cf/test/phil-test.json'):
        os.remove('/usr/local/var/keri/cf/test/phil-test.json')
    if os.path.exists('/usr/local/var/keri/db/test/phil-test'):
        shutil.rmtree('/usr/local/var/keri/db/test/phil-test')
    if os.path.exists('/usr/local/var/keri/ks/test/phil-test'):
        shutil.rmtree('/usr/local/var/keri/ks/test/phil-test')

    name = "phil-test"

    with habbing.openHby(name=name, base="test", temp=False) as hby:
        hab = hby.makeHab(name=name, icount=1, wits=["BANkPDTGELcUDH-TBCEjo4dpCvUnO_DnOSNEaNlL--4M"])
        oidig = hab.iserder.said
        opre = hab.pre
        opub = hab.kever.verfers[0].qb64
        odig = hab.kever.serder.said

    with habbing.openHby(name=name, base="test", temp=False) as hby:
        hab = hby.habByName(name)
        assert hab.pre == opre
        assert hab.prefixes is hab.db.prefixes
        assert hab.kevers is hab.db.kevers
        assert hab.pre in hab.prefixes
        assert hab.pre in hab.kevers
        assert hab.iserder.said == oidig

        hab.rotate(ncount=3)
        assert opub != hab.kever.verfers[0].qb64
        assert odig != hab.kever.serder.said

    hby.close(clear=True)
    hby.cf.close(clear=True)
    assert not os.path.exists(hby.cf.path)
    assert not os.path.exists(hby.db.path)
    assert not os.path.exists(hby.ks.path)


def test_habery_reinitialization():
    """Test Reinitializing Habery and its Habs
    """

    if os.path.exists('/usr/local/var/keri/cf/test/bob-test.json'):
        os.remove('/usr/local/var/keri/cf/test/bob-test.json')
    if os.path.exists('/usr/local/var/keri/db/test/bob-test'):
        shutil.rmtree('/usr/local/var/keri/db/test/bob-test')
    if os.path.exists('/usr/local/var/keri/ks/test/bob-test'):
        shutil.rmtree('/usr/local/var/keri/ks/test/bob-test')

    name = "bob-test"

    with habbing.openHby(name=name, base="test", temp=False, clear=True) as hby:
        hab = hby.makeHab(name=name, icount=1)
        oidig = hab.iserder.said
        opre = hab.pre
        opub = hab.kever.verfers[0].qb64
        odig = hab.kever.serder.said

    with habbing.openHby(name=name, base="test", temp=False) as hby:

        assert opre in hby.db.kevers  # read through cache
        assert opre in hby.db.prefixes

        hab = hby.habByName(name)
        assert hab.pre == opre
        assert hab.prefixes is hab.db.prefixes
        assert hab.kevers is hab.db.kevers
        assert hab.pre in hab.prefixes
        assert hab.pre in hab.kevers
        assert hab.iserder.said == oidig

        hab.rotate()
        assert opub != hab.kever.verfers[0].qb64
        assert odig != hab.kever.serder.said

        npub = hab.kever.verfers[0].qb64
        ndig = hab.kever.serder.said

        assert opre == hab.pre
        assert hab.kever.verfers[0].qb64 == npub
        assert hab.kever.serder.said != odig
        assert hab.kever.serder.said == ndig

    hby.close(clear=True)
    hby.cf.close(clear=True)
    assert not os.path.exists(hby.cf.path)
    assert not os.path.exists(hby.db.path)
    assert not os.path.exists(hby.ks.path)

    """End Test"""


def test_habery_signatory():
    with habbing.openHby(salt=coring.Salter(raw=b'0123456789abcdef').qb64) as hby:
        signer = hby.signator

        assert signer is not None
        assert signer.pre == 'BN5Lu0RqptmJC-iXEldMMrlEew7Q01te2fLgqlbqW9zR'

        # Assert we get the same one in subsequent calls
        sig2 = hby.signator
        assert sig2 == signer
        raw = b'this is the raw data'

        # Sign some data
        cig = signer.sign(ser=raw)
        assert cig.qb64b == (b'0BBcREN6U3eyPXDnRaDrRBgA7JECxr8fAqTHvbLY8RzMBIQr1'
                             b'Qoz9H5d0aPM1EbKFP1DcT1zadxbeEQciT0lkysL')

        # Verify the signature
        assert signer.verify(ser=raw, cigar=cig) is True

        # Make sure this new key doesn't effect the habery environment
        assert len(hby.habs) == 0
        assert len(hby.prefixes) == 0


def test_habery_reconfigure(mockHelpingNowUTC):
    """
    Test   .reconfigure method using .cf for config file

     conf
    {
      dt: "isodatetime",
      curls: ["tcp://localhost:5620/"],
      iurls: ["ftp://localhost:5621/?name=eve"],
    }

    """
    # use same salter but with different path from name for each
    # salt = pysodium.randombytes(pysodium.crypto_pwhash_SALTBYTES)
    # raw = b'\x05\xaa\x8f-S\x9a\xe9\xfaU\x9c\x02\x9c\x9b\x08Hu'
    # salter = coring.Salter(raw=raw)
    # salt = salter.qb64
    # assert salt == '0ABaqPLVOa6fpVnAKcmwhIdQ'

    salt = coring.Salter(raw=b'0123456789abcdef').qb64

    cname = "tam"  # controller name
    cbase = "main"  # controller base shared
    pname = "nel"  # peer name
    pbase = "head"  # peer base shared

    with (habbing.openHby(name='wes', base=cbase, salt=salt) as wesHby,
          habbing.openHby(name='wok', base=cbase, salt=salt) as wokHby,
          habbing.openHby(name=cname, base=cbase, salt=salt) as tamHby,
          habbing.openHby(name='wat', base=cbase, salt=salt) as watHby,
          habbing.openHby(name=pname, base=pbase, salt=salt) as nelHby):
        # witnesses first so can setup inception event for tam
        wsith = '1'

        # setup Wes's habitat nontrans
        wesHab = wesHby.makeHab(name="wes", isith=wsith, icount=1, transferable=False)
        assert not wesHab.kever.prefixer.transferable

        # setup Wok's habitat nontrans
        wokHab = wokHby.makeHab(name="wok", isith=wsith, icount=1, transferable=False)
        assert not wokHab.kever.prefixer.transferable

        # setup Tam's config
        curls = ["tcp://localhost:5620/"]
        iurls = [f"tcp://localhost:5621/?role={kering.Roles.peer}&name={pname}"]
        assert tamHby.cf.get() == {}
        conf = dict(dt=help.nowIso8601(), tam=dict(dt=help.nowIso8601(), curls=curls), iurls=iurls)
        tamHby.cf.put(conf)

        assert tamHby.cf.get() == {'dt': '2021-01-01T00:00:00.000000+00:00',
                                   'tam': {
                                       'dt': '2021-01-01T00:00:00.000000+00:00',
                                       'curls': ['tcp://localhost:5620/']
                                   },
                                   'iurls': ['tcp://localhost:5621/?role=peer&name=nel']}

        # setup Tam's habitat trans multisig
        wits = [wesHab.pre, wokHab.pre]
        tsith = '1'  # hex str of threshold int
        tamHab = tamHby.makeHab(name=cname, isith=tsith, icount=3, toad=2, wits=wits)
        assert tamHab.kever.prefixer.transferable
        assert len(tamHab.iserder.berfers) == len(wits)
        for werfer in tamHab.iserder.berfers:
            assert werfer.qb64 in wits
        assert tamHab.kever.wits == wits
        assert tamHab.kever.toader.num == 2
        assert tamHab.kever.sn == 0
        assert tamHab.kever.tholder.thold == 1 == int(tsith, 16)
        # create non-local kevery for Tam to process non-local msgs

        # check tamHab.cf config setup
        ender = tamHab.db.ends.get(keys=(tamHab.pre, "controller", tamHab.pre))
        assert ender.allowed
        assert not ender.name
        locer = tamHab.db.locs.get(keys=(tamHab.pre, kering.Schemes.tcp))
        assert locer.url == 'tcp://localhost:5620/'

        # setup Wat's habitat nontrans
        watHab = watHby.makeHab(name="wat", isith=wsith, icount=1, transferable=False, )
        assert not watHab.kever.prefixer.transferable

        # setup Nel's config
        curls = ["tcp://localhost:5621/"]
        iurls = [f"tcp://localhost:5620/?role={kering.Roles.peer}&name={cname}"]
        assert nelHby.cf.get() == {}
        conf = dict(dt=help.nowIso8601(), nel=dict(dt=help.nowIso8601(), curls=curls), iurls=iurls)
        nelHby.cf.put(conf)

        assert nelHby.cf.get() == {'dt': '2021-01-01T00:00:00.000000+00:00',
                                   'nel': {
                                       'dt': '2021-01-01T00:00:00.000000+00:00',
                                       'curls': ['tcp://localhost:5621/'],
                                   },
                                   'iurls': ['tcp://localhost:5620/?role=peer&name=tam']}

        # setup Nel's habitat nontrans
        nelHab = nelHby.makeHab(name=pname, isith=wsith, icount=1, transferable=False)
        assert not nelHab.kever.prefixer.transferable
        # create non-local parer for Nel to process non-local msgs

        assert nelHab.pre == 'BBWmLeVPY4obmPkyBGCsmysDmhbe017t6gS7v6B_ogV9'
        assert nelHab.kever.prefixer.code == coring.MtrDex.Ed25519N
        assert nelHab.kever.verfers[0].qb64 == nelHab.pre

        # check nelHab.cf config setup
        ender = nelHab.db.ends.get(keys=(nelHab.pre, "controller", nelHab.pre))
        assert ender.allowed
        assert not ender.name
        locer = nelHab.db.locs.get(keys=(nelHab.pre, kering.Schemes.tcp))
        assert locer.url == 'tcp://localhost:5621/'

    assert not os.path.exists(nelHby.cf.path)
    assert not os.path.exists(nelHby.db.path)
    assert not os.path.exists(nelHby.ks.path)
    assert not os.path.exists(watHby.cf.path)
    assert not os.path.exists(watHby.db.path)
    assert not os.path.exists(watHby.ks.path)
    assert not os.path.exists(wokHby.cf.path)
    assert not os.path.exists(wokHby.db.path)
    assert not os.path.exists(wokHby.ks.path)
    assert not os.path.exists(wesHby.cf.path)
    assert not os.path.exists(wesHby.db.path)
    assert not os.path.exists(wesHby.ks.path)
    assert not os.path.exists(tamHby.cf.path)
    assert not os.path.exists(tamHby.db.path)
    assert not os.path.exists(tamHby.ks.path)
    """Done Test"""


def test_namespaced_habs():
    with habbing.openHby(salt=coring.Salter(raw=b'0123456789abcdef').qb64) as hby:
        hab = hby.makeHab(name="test")
        assert hab.pre == "EIaGMMWJFPmtXznY1IIiKDIrg-vIyge6mBl2QV8dDjI3"

        found = hby.habByName("test")
        assert found.pre == "EIaGMMWJFPmtXznY1IIiKDIrg-vIyge6mBl2QV8dDjI3"

        assert len(hby.habs) == 1
        assert len(hby.prefixes) == 1

        nshab = hby.makeHab(name="test2", ns="agent")
        assert nshab.pre == "EErXOolQNmKrTMKfXdQ1sj8YsgZZe4wMXZwsX-j1V6Dd"

        assert len(hby.habs) == 1
        assert len(hby.namespaces) == 1
        assert len(hby.prefixes) == 2

        found = hby.habByName(name="test2")
        assert found is None
        found = hby.habByName(name="test2", ns="agent")
        assert found.pre == "EErXOolQNmKrTMKfXdQ1sj8YsgZZe4wMXZwsX-j1V6Dd"
        found = hby.habByName(name="test", ns="agent")
        assert found is None

        # Test a '.' in Hab name
        nshab = hby.makeHab(name="test.3", ns="agent")
        assert nshab.pre == "EG5FUOzW_KKVB8JGlNGoZAADDC8cZ6Jt079nLEaFnYcg"

        assert len(hby.habs) == 1
        assert len(hby.namespaces) == 1
        assert len(hby.prefixes) == 3
        ns = hby.namespaces['agent']
        assert len(ns) == 2

        # '.' characters not allowed in namespace names
        with pytest.raises(kering.ConfigurationError):
            hby.makeHab(name="test", ns="agent.5")

    hby.close()

    # Test Reload of Namespace habs
    name = "ns-test"
    with habbing.openHby(name=name, base="test", temp=False, clear=True) as hby:
        hab = hby.makeHab(name=name, icount=1)
        opre = hab.pre
        hab = hby.makeHab(name="test.1", icount=1)
        o2pre = hab.pre
        nshab = hby.makeHab(name="test", ns="agent")
        atpre = nshab.pre
        nshab = hby.makeHab(name="test2", ns="agent")
        at2pre = nshab.pre
        nshab = hby.makeHab(name="test", ns="controller")
        ctpre = nshab.pre

    with habbing.openHby(name=name, base="test", temp=False) as hby:
        for pre in [opre, o2pre, atpre, at2pre, ctpre]:
            assert pre in hby.db.kevers  # read through cache
            assert pre in hby.db.prefixes

        assert len(hby.habs) == 2
        assert len(hby.db.prefixes) == 5

        agent = hby.namespaces["agent"]
        assert len(agent) == 2
        ctrl = hby.namespaces["controller"]
        assert len(ctrl) == 1

        found = hby.habByName(name=name)
        assert found.pre == opre
        found = hby.habByName(name="test.1")
        assert found.pre == o2pre
        found = hby.habByName(name="test", ns="agent")
        assert found.pre == atpre
        found = hby.habByName(name="test2", ns="agent")
        assert found.pre == at2pre
        found = hby.habByName(name="test", ns="controller")
        assert found.pre == ctpre

    hby.close(clear=True)
    hby.cf.close(clear=True)


def test_make_other_event():
    with habbing.openHby(salt=coring.Salter(raw=b'0123456789abcdef').qb64) as hby:
        hab = hby.makeHab(name="test")
        assert hab.pre == "EIaGMMWJFPmtXznY1IIiKDIrg-vIyge6mBl2QV8dDjI3"

        hab.rotate()
        hab.rotate()

        msg = hab.makeOtherEvent(hab.pre, sn=1)
        assert msg == (b'{"v":"KERI10JSON000160_","t":"rot","d":"EGnFNzw2UJKpQZYJj_xhcFYW'
                       b'E7prFWFBbghgcMuJ4VeM","i":"EIaGMMWJFPmtXznY1IIiKDIrg-vIyge6mBl2Q'
                       b'V8dDjI3","s":"1","p":"EIaGMMWJFPmtXznY1IIiKDIrg-vIyge6mBl2QV8dDj'
                       b'I3","kt":"1","k":["DGgN_X4ZJvgAMQpD3CqI5bidKkgkCLc_yk-Pk1culnXP"'
                       b'],"nt":"1","n":["EOh7LXjpAqsP6YNGOMVFjn02yCpXfGVsHbSYIQ5Ul7Ax"],'
                       b'"bt":"0","br":[],"ba":[],"a":[]}-AABAAC2DAJCt6KLh442NsGVLE0pYKvL'
                       b'-3MVh-kWcBWWqpVmXbhlQ3oGHD5h4jUY7Trw2jFvsQyC4A_1kJpmNP1AgXcM')

        msg = hab.makeOtherEvent(hab.pre, sn=2)
        assert msg == (b'{"v":"KERI10JSON000160_","t":"rot","d":"EJCaUsmfvR35xZxpenqEWCtX'
                       b'sXnD_efjlvvRd1hEvu5d","i":"EIaGMMWJFPmtXznY1IIiKDIrg-vIyge6mBl2Q'
                       b'V8dDjI3","s":"2","p":"EGnFNzw2UJKpQZYJj_xhcFYWE7prFWFBbghgcMuJ4V'
                       b'eM","kt":"1","k":["DPjsUEx6Nqby9-yUO1DtExQ81CRYdvpwQZufBRzBM5yk"'
                       b'],"nt":"1","n":["EIraDaPWlGBU9DnwCaNQ2XVaX8zQQFhnkj8Ir4R5R-Yh"],'
                       b'"bt":"0","br":[],"ba":[],"a":[]}-AABAADGsMs4ifEPuBH9vApQTnJyGCXm'
                       b'p8Sc4CcESKA-q5O0O5CmpCbSrA29UpqZnfvUagrwm8w3M1a1WJKy64OQYXIG')


def test_hab_by_pre():
    with habbing.openHby() as hby:
        # Create two habs in the default namespace
        hab1 = hby.makeHab(name="test1")
        hab2 = hby.makeHab(name="test2")

        # Create two habs in namespace "one"
        hab3 = hby.makeHab(name="test1", ns="one")
        hab4 = hby.makeHab(name="test2", ns="one")

        # Create two habs in namespace "two"
        hab5 = hby.makeHab(name="test1", ns="two")
        hab6 = hby.makeHab(name="test2", ns="two")

        # Only habs in default namespace are in hby.habs
        assert hab1.pre in hby.habs
        assert hab2.pre in hby.habs
        assert hab3.pre not in hby.habs
        assert hab4.pre not in hby.habs
        assert hab5.pre not in hby.habs
        assert hab6.pre not in hby.habs

        assert hby.habByPre("EIaGMMWJFPmtXznY1IIiKDIrg-vIyge6mBl2QV8dDjI3") is None

        assert hby.habByPre(pre=hab1.pre) == hab1
        assert hby.habByPre(pre=hab2.pre) == hab2
        assert hby.habByPre(pre=hab3.pre) == hab3
        assert hby.habByPre(pre=hab4.pre) == hab4
        assert hby.habByPre(pre=hab5.pre) == hab5
        assert hby.habByPre(pre=hab6.pre) == hab6

        assert "one" in hby.namespaces
        assert hab3.pre in hby.namespaces["one"]
        assert hab4.pre in hby.namespaces["one"]
        assert hab1.pre not in hby.namespaces["one"]
        assert hab2.pre not in hby.namespaces["one"]
        assert "two" in hby.namespaces
        assert hab5.pre in hby.namespaces["two"]
        assert hab6.pre in hby.namespaces["two"]
        assert hab1.pre not in hby.namespaces["two"]
        assert hab2.pre not in hby.namespaces["two"]


def test_postman_endsfor():
    with habbing.openHby(name="test", temp=True, salt=coring.Salter(raw=b'0123456789abcdef').qb64) as hby, \
            habbing.openHby(name="wes", temp=True, salt=coring.Salter(raw=b'wess-the-witness').qb64) as wesHby, \
            habbing.openHab(name="agent", temp=True, salt=b'0123456789abcdef') as (agentHby, agentHab):

        wesHab = wesHby.makeHab(name='wes', isith="1", icount=1, transferable=False)
        assert not wesHab.kever.prefixer.transferable
        # create non-local kevery for Wes to process nonlocal msgs
        wesKvy = eventing.Kevery(db=wesHab.db, lax=False, local=False)

        wits = [wesHab.pre]
        hab = hby.makeHab(name='cam', isith="1", icount=1, toad=1, wits=wits, )
        assert hab.kever.prefixer.transferable
        assert len(hab.iserder.berfers) == len(wits)
        for werfer in hab.iserder.berfers:
            assert werfer.qb64 in wits
        assert hab.kever.wits == wits
        assert hab.kever.toader.num == 1
        assert hab.kever.sn == 0

        kvy = eventing.Kevery(db=hab.db, lax=False, local=False)
        icpMsg = hab.makeOwnInception()
        rctMsgs = []  # list of receipts from each witness
        parsing.Parser().parse(ims=bytearray(icpMsg), kvy=wesKvy, local=True)
        assert wesKvy.kevers[hab.pre].sn == 0  # accepted event
        assert len(wesKvy.cues) >= 1  # assunmes includes queued receipt cue
        # better to find cue in cues and confirm exactly
        rctMsg = wesHab.processCues(wesKvy.cues)  # process cue returns rct msg
        assert len(rctMsg) == 626
        rctMsgs.append(rctMsg)

        for msg in rctMsgs:  # process rct msgs from all witnesses
            parsing.Parser().parse(ims=bytearray(msg), kvy=kvy, local=True)
        assert wesHab.pre in kvy.kevers

        agentIcpMsg = agentHab.makeOwnInception()
        parsing.Parser().parse(ims=bytearray(agentIcpMsg), kvy=kvy, local=True)
        assert agentHab.pre in kvy.kevers

        msgs = bytearray()
        msgs.extend(wesHab.makeEndRole(eid=wesHab.pre,
                                       role=kering.Roles.controller,
                                       stamp=helping.nowIso8601()))

        msgs.extend(wesHab.makeLocScheme(url='http://127.0.0.1:8888',
                                         scheme=kering.Schemes.http,
                                         stamp=helping.nowIso8601()))
        wesHab.psr.parse(ims=bytearray(msgs))

        # Set up
        msgs.extend(hab.makeEndRole(eid=hab.pre,
                                    role=kering.Roles.controller,
                                    stamp=helping.nowIso8601()))

        msgs.extend(hab.makeLocScheme(url='http://127.0.0.1:7777',
                                      scheme=kering.Schemes.http,
                                      stamp=helping.nowIso8601()))
        hab.psr.parse(ims=msgs)

        msgs = bytearray()
        msgs.extend(agentHab.makeEndRole(eid=agentHab.pre,
                                         role=kering.Roles.controller,
                                         stamp=helping.nowIso8601()))

        msgs.extend(agentHab.makeLocScheme(url='http://127.0.0.1:6666',
                                           scheme=kering.Schemes.http,
                                           stamp=helping.nowIso8601()))

        msgs.extend(hab.makeEndRole(eid=agentHab.pre,
                                    role=kering.Roles.agent,
                                    stamp=helping.nowIso8601()))

        msgs.extend(hab.makeEndRole(eid=agentHab.pre,
                                    role=kering.Roles.mailbox,
                                    stamp=helping.nowIso8601()))

        agentHab.psr.parse(ims=bytearray(msgs))
        hab.psr.parse(ims=bytearray(msgs))

        ends = hab.endsFor(hab.pre)
        assert ends == {
            'agent': {
                'EBErgFZoM3PBQNTpTuK9bax_U8HLJq1Re2RM1cdifaTJ': {'http': 'http://127.0.0.1:6666'}},
            'controller': {
                'EGadHcyW9IfVIPrFUAa_I0z4dF8QzQAvUvfaUTJk8Jre': {'http': 'http://127.0.0.1:7777'}},
            'mailbox': {
                'EBErgFZoM3PBQNTpTuK9bax_U8HLJq1Re2RM1cdifaTJ': {'http': 'http://127.0.0.1:6666'}},
            'witness': {
                'BN8t3n1lxcV0SWGJIIF46fpSUqA7Mqre5KJNN3nbx3mr': {'http': 'http://127.0.0.1:8888'}}
        }


if __name__ == "__main__":
    pass
    test_habery()
    # pytest.main(['-vv', 'test_habbing.py::test_habery_reconfigure'])
