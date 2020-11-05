import setuptools
from setuptools.extension import Extension
from distutils.command.build_ext import build_ext as DistUtilsBuildExt


class BuildExtension(setuptools.Command):
    description = DistUtilsBuildExt.description
    user_options = DistUtilsBuildExt.user_options
    boolean_options = DistUtilsBuildExt.boolean_options
    help_options = DistUtilsBuildExt.help_options

    def __init__(self, *args, **kwargs):
        """
        Initialize the extension.

        Args:
            self: (todo): write your description
        """
        from setuptools.command.build_ext import build_ext as SetupToolsBuildExt

        # Bypass __setatrr__ to avoid infinite recursion.
        self.__dict__['_command'] = SetupToolsBuildExt(*args, **kwargs)

    def __getattr__(self, name):
        """
        Returns the value of the given name.

        Args:
            self: (todo): write your description
            name: (str): write your description
        """
        return getattr(self._command, name)

    def __setattr__(self, name, value):
        """
        Sets the value.

        Args:
            self: (todo): write your description
            name: (str): write your description
            value: (todo): write your description
        """
        setattr(self._command, name, value)

    def initialize_options(self, *args, **kwargs):
        """
        Initialize command options.

        Args:
            self: (todo): write your description
        """
        return self._command.initialize_options(*args, **kwargs)

    def finalize_options(self, *args, **kwargs):
        """
        Finalize command line options.

        Args:
            self: (todo): write your description
        """
        ret = self._command.finalize_options(*args, **kwargs)
        import numpy
        self.include_dirs.append(numpy.get_include())
        return ret

    def run(self, *args, **kwargs):
        """
        Run the command.

        Args:
            self: (todo): write your description
        """
        return self._command.run(*args, **kwargs)


extensions = [
    Extension(
        'utils.compute_overlap',
        ['utils/compute_overlap.pyx']
    ),
]

setuptools.setup(
    cmdclass={'build_ext': BuildExtension},
    packages=setuptools.find_packages(),
    ext_modules=extensions,
    setup_requires=["cython>=0.28", "numpy>=1.14.0"]
)
