"""

"""

__name__ = 'simple_rec'
__version__ = '0.0.1'


try:
    # See (https://github.com/PyTorchLightning/pytorch-lightning)
    # This variable is injected in the __builtins__ by the build
    # process. It used to enable importing subpackages of skimage when
    # the binaries are not built
    __SIMPLE_REC_SETUP__
except NameError:
    __SIMPLE_REC_SETUP__ = False


if __SIMPLE_REC_SETUP__:
    # setting up simple_rec
    msg = f'Partial import of {__name__}=={__version__} during build process.' 
    print(msg)
else:
    from simple_rec import compute
    from simple_rec import filters
    from simple_rec.filters.collaborative import CollaborativeFilter