
from generalfile import Path
from generalfile.test.test_path import PathTest

class FileTest(PathTest):
    def test_cfg(self):
        dict_ = {'setup': {'name': 'generalfile', 'version': '2.2.3', 'description': 'Easily manage files cross platform.', 'install_requires': '["generallibrary", "send2trash", "appdirs"]', 'extras_require': '{\n"spreadsheet": ["pandas"]\n}', 'classifiers': '[\n"Development Status :: 2 - Pre-Alpha",\n"Topic :: Desktop Environment :: File Managers"\n]'}}

        Path("foo").cfg.write(dict_)
        self.assertEqual(dict_, Path("foo").cfg.read())

        dict_["setup"]["name"] = "test"

        Path("foo").cfg.write(dict_, overwrite=True)
        self.assertEqual(dict_, Path("foo").cfg.read())

    def test_cfg_append(self):
        dict_ = {'setup': {'hello': 'random'}}
        Path("foo").cfg.write(dict_)

        dict_ = {'setup': {'foo': 'random'}, "test": {5: "bar"}}
        Path("foo").cfg.append(dict_)

        self.assertEqual({'setup': {'foo': 'random'}, 'test': {'5': 'bar'}}, Path("foo").cfg.read())


