try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='customnoseplugins',
    version="4.0.2",
    description = 'test plan plugins for the nose testing framework',
    author = 'bao hongbin',
    author_email = 'hongbin.bao@gmail.com',
    license = 'MIT',
    long_description = """
    Extra plugins for the nose testing framework to load test case from a plan file and specify the execute order in test suite\n
    """,
    packages = ['customnoseplugins'],
    entry_points = {
        'nose.plugins': [
            'plan-loader = customnoseplugins.planloader:PlanLoaderPlugin',
            'file-output = customnoseplugins.fileoutput:FileOutputPlugin',
            ],
    },
)
