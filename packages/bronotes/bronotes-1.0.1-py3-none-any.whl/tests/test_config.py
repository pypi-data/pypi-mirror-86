# TODO Expand on this with something that tests the config file.
class TestConfig():

    def test_constructor(self, cfg_fixt, dir_fixt):
        assert cfg_fixt.dir == dir_fixt
