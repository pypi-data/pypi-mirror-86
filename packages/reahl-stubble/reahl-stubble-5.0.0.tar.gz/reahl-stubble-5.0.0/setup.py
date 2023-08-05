from setuptools import setup, Command
class InstallTestDependencies(Command):
    user_options = []
    def run(self):
        import sys
        import subprocess
        if self.distribution.tests_require: subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"]+self.distribution.tests_require)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

setup(
    name='reahl-stubble',
    version='5.0.0',
    description='Stub tools for use in unit testing',
    long_description='Reahl is a web application framework that allows a Python programmer to work in terms of useful abstractions - using a single programming language.\n\nStubble (a part of the Reahl development tools) is a collection of tools for writing stubs in unit tests. Stubble can be used independently of the Reahl web framework.\n\nUsing stubs allows one to decouple one unit test from real code unrelated to it - you write a fake class to take the place of a real one (which this test is not testing).\n\nStubble ensures, however, that the test will break should the interface of the stub differ from that of the real class it is a stub for. ',
    url='http://www.reahl.org',
    maintainer='Iwan Vosloo',
    maintainer_email='iwan@reahl.org',
    packages=['examples', 'reahl', 'reahl.stubble', 'reahl.stubble_dev'],
    py_modules=[],
    include_package_data=False,
    package_data={'': ['*/LC_MESSAGES/*.mo']},
    namespace_packages=['reahl'],
    install_requires=['setuptools>=32.3.1'],
    setup_requires=['setuptools-git>=1.1', 'pytest-runner', 'pip>=10.0.0'],
    tests_require=['pytest>=3.0'],
    test_suite='reahl.stubble_dev',
    entry_points={
        'reahl.versions': [
            '5.0 = 5.0',
            '4.0 = 4.0',
            '3.2 = 3.2',
            '3.1 = 3.1',
            '3.0 = 3.0',
            '2.1 = 2.1',
            '2.0 = 2.0'    ],
        'reahl.versiondeps.5.0': [
            'setuptools = thirdpartyegg:32.3.1'    ],
        'reahl.versiondeps.4.0': [
            'six = thirdpartyegg:_',
            'setuptools = thirdpartyegg:32.3.1'    ],
        'reahl.versiondeps.3.2': [
            'six = thirdpartyegg:_'    ],
        'reahl.versiondeps.3.1': [
            'six = thirdpartyegg:_'    ],
        'reahl.eggs': [
            'Egg = reahl.component.eggs:ReahlEgg'    ],
                 },
    extras_require={},
    cmdclass={'install_test_dependencies': InstallTestDependencies}
)
