import filecmp
import os
import shutil
import sys
import tempfile
import configargparse
import unittest
import ct.unittesthelper

try:
    # This call to reload is simply to test
    # that reload is in the current namespace
    reload(unittest)
except NameError:
    from importlib import reload

import ct.unittesthelper as uth
import ct.wrappedos
import ct.headerdeps
import ct.magicflags
import ct.hunter


def callprocess(headerobj, filenames):
    result = set()
    for filename in filenames:
        realpath = ct.wrappedos.realpath(filename)
        result |= headerobj.process(realpath)
    return result


def _reload_ct(cache_home):
    """ Set the CTCACHE environment variable to cache_home
        and reload the ct.* modules
    """
    os.environ["CTCACHE"] = cache_home
    reload(ct.headerdeps)
    reload(ct.magicflags)
    reload(ct.hunter)


class TestHunterModule(unittest.TestCase):
    def setUp(self):
        uth.reset()
        cap = configargparse.getArgumentParser(
            description="Configargparser in test code",
            formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
            args_for_setting_config_path=["-c", "--config"],
            ignore_unknown_config_file_keys=False,
        )

    def test_hunter_follows_source_files_from_header(self):
        origcache = ct.dirnamer.user_cache_dir("ct")
        tempdir = tempfile.mkdtemp()
        _reload_ct(tempdir)

        temp_config = ct.unittesthelper.create_temp_config()
        argv = ["-c", temp_config, "--include", uth.ctdir()]
        cap = configargparse.getArgumentParser()
        ct.hunter.add_arguments(cap)
        args = ct.apptools.parseargs(cap, argv)
        headerdeps = ct.headerdeps.create(args)
        magicparser = ct.magicflags.create(args, headerdeps)
        hntr = ct.hunter.Hunter(args, headerdeps, magicparser)

        relativepath = "factory/widget_factory.hpp"
        realpath = os.path.join(uth.samplesdir(), relativepath)
        filesfromheader = hntr.required_source_files(realpath)
        filesfromsource = hntr.required_source_files(ct.utils.implied_source(realpath))
        self.assertSetEqual(filesfromheader, filesfromsource)

        # Cleanup
        os.unlink(temp_config)
        shutil.rmtree(tempdir)
        _reload_ct(origcache)

    @staticmethod
    def _hunter_is_not_order_dependent(precall):
        samplesdir = uth.samplesdir()
        relativepaths = [
            "factory/test_factory.cpp",
            "numbers/test_direct_include.cpp",
            "simple/helloworld_c.c",
            "simple/helloworld_cpp.cpp",
            "simple/test_cflags.c",
        ]
        bulkpaths = [os.path.join(samplesdir, filename) for filename in relativepaths]
        temp_config = ct.unittesthelper.create_temp_config()
        argv = ["--config", temp_config, "--include", uth.ctdir()]
        cap = configargparse.getArgumentParser()
        ct.hunter.add_arguments(cap)
        args = ct.apptools.parseargs(cap, argv)
        headerdeps = ct.headerdeps.create(args)
        magicparser = ct.magicflags.create(args, headerdeps)
        hntr = ct.hunter.Hunter(args, headerdeps, magicparser)
        os.unlink(temp_config)

        realpath = os.path.join(samplesdir, "dottypaths/dottypaths.cpp")
        if precall:
            result = hntr.required_source_files(realpath)
            return result
        else:
            for filename in bulkpaths:
                discard = hntr.required_source_files(filename)
            result = hntr.required_source_files(realpath)
            return result

    def test_hunter_is_not_order_dependent(self):
        origcache = ct.dirnamer.user_cache_dir("ct")
        tempdir = tempfile.mkdtemp()
        _reload_ct(tempdir)

        result2 = self._hunter_is_not_order_dependent(True)
        result1 = self._hunter_is_not_order_dependent(False)
        result3 = self._hunter_is_not_order_dependent(False)
        result4 = self._hunter_is_not_order_dependent(True)

        self.assertSetEqual(result1, result2)
        self.assertSetEqual(result3, result2)
        self.assertSetEqual(result4, result2)

        # Cleanup
        shutil.rmtree(tempdir)
        _reload_ct(origcache)

    def tearDown(self):
        uth.reset()


if __name__ == "__main__":
    unittest.main()
