"""Had the following error: when parametrizing a name and a string containing the exact same value as identifier of said name, 
only the first occuring of these of them would appear. Due to bad logic in the __str__() method of class NodeDifference. Fixed 15.03.24"""

class TestSkipMember:
    def assert_skip(self, what, member, obj, expect_default_skip, config_name):
        skip = True
        app = mock.Mock()
        app.config = Config()
        setattr(app.config, config_name, True)
        if expect_default_skip:
            assert None is _skip_member(app, what, member, obj, skip, mock.Mock())
        else:
            assert _skip_member(app, what, member, obj, skip, mock.Mock()) is False
        setattr(app.config, config_name, False)
        assert None is _skip_member(app, what, member, obj, skip, mock.Mock())

    def test_namedtuple(self):
        # Since python 3.7, namedtuple._asdict() has not been documented
        # because there is no way to check the method is a member of the
        # namedtuple class.  This testcase confirms only it does not
        # raise an error on building document (refs: #1455)
        self.assert_skip('class', '_asdict',
                         SampleNamedTuple._asdict, True,
                         'napoleon_include_private_with_doc')

    def test_class_private_doc(self):
        self.assert_skip('class', '_private_doc',
                         SampleClass._private_doc, False,
                         'napoleon_include_private_with_doc')

    def test_class_private_undoc(self):
        self.assert_skip('class', '_private_undoc',
                         SampleClass._private_undoc, True,
                         'napoleon_include_private_with_doc')

    def test_class_special_doc(self):
        self.assert_skip('class', '__special_doc__',
                         SampleClass.__special_doc__, False,
                         'napoleon_include_special_with_doc')

    def test_class_special_undoc(self):
        self.assert_skip('class', '__special_undoc__',
                         SampleClass.__special_undoc__, True,
                         'napoleon_include_special_with_doc')

    def test_class_decorated_doc(self):
        self.assert_skip('class', '__decorated_func__',
                         SampleClass.__decorated_func__, False,
                         'napoleon_include_special_with_doc')

    def test_exception_private_doc(self):
        self.assert_skip('exception', '_private_doc',
                         SampleError._private_doc, False,
                         'napoleon_include_private_with_doc')

    def test_exception_private_undoc(self):
        self.assert_skip('exception', '_private_undoc',
                         SampleError._private_undoc, True,
                         'napoleon_include_private_with_doc')

    def test_exception_special_doc(self):
        self.assert_skip('exception', '__special_doc__',
                         SampleError.__special_doc__, False,
                         'napoleon_include_special_with_doc')

    def test_exception_special_undoc(self):
        self.assert_skip('exception', '__special_undoc__',
                         SampleError.__special_undoc__, True,
                         'napoleon_include_special_with_doc')

    def test_module_private_doc(self):
        self.assert_skip('module', '_private_doc', _private_doc, False,
                         'napoleon_include_private_with_doc')

    def test_module_private_undoc(self):
        self.assert_skip('module', '_private_undoc', _private_undoc, True,
                         'napoleon_include_private_with_doc')

    def test_module_special_doc(self):
        self.assert_skip('module', '__special_doc__', __special_doc__, False,
                         'napoleon_include_special_with_doc')

    def test_module_special_undoc(self):
        self.assert_skip('module', '__special_undoc__', __special_undoc__, True,
                         'napoleon_include_special_with_doc')