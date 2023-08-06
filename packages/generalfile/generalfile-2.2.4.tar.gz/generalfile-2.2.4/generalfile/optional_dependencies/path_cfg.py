
from generallibrary import deco_cache, initBases

import configparser


class Path_Cfg:
    """ Cfg methods for Path. """
    @property
    @deco_cache()
    def cfg(self):
        """ Easily read and write to cfg files with a dictionary.
            Easy access to a dynamically one-time created Cfg class, initalized with self (Path). """
        return self._cfg()(self)

    @staticmethod
    @deco_cache()
    def _cfg():
        @initBases
        class _Cfg(_Extension):
            def write(self, dict_=None, overwrite=False):
                """ Write to this path with a given dictionary. """
                with self.WriteContext(self.path, overwrite=overwrite) as write_path:
                    with open(str(write_path), "w") as file:
                        config = configparser.RawConfigParser()
                        config.read_dict(dictionary=dict_)
                        config.write(file)

            def read(self):
                """ Read from this path to get a dictionary. """
                with self.ReadContext(self.path) as read_path:
                    config = configparser.RawConfigParser()
                    config.read(str(read_path))
                    return {s: dict(config.items(s)) for s in config.sections()}

            def append(self, dict_):
                """ Update this cfg with a dictionary. """
                with self.AppendContext(self.path) as append_path:
                    read = append_path.cfg.read()
                    read.update(dict_)
                    append_path.cfg.write(dict_=dict_, overwrite=True)

        return _Cfg


from generalfile.path_operations import _Extension






































