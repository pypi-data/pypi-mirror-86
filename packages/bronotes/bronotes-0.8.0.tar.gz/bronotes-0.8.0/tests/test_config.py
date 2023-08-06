class TestConfig():

    def test_constructor(self, cfg_fixt, dir_fixt):
        assert cfg_fixt.dir == dir_fixt
