import pytest


class TestSystemReader:

    def test_super_class_implementation(self):
        from cmdb.utils.system_reader import SystemReader
        system_reader_super_instance = SystemReader()
        with pytest.raises(NotImplementedError):
            system_reader_super_instance.get_value('test', 'test')
        with pytest.raises(NotImplementedError):
            system_reader_super_instance.get_sections()
        with pytest.raises(NotImplementedError):
            system_reader_super_instance.get_all_values_from_section('test')
        with pytest.raises(NotImplementedError):
            system_reader_super_instance.setup()


class TestSystemConfigReader:

    def test_config_less_instance(self):
        from cmdb.utils.system_reader import SystemConfigReader
        system_config_reader = SystemConfigReader()
        assert system_config_reader.config_file_less is True
