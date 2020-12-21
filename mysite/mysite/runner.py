class PytestTestRunner:
    """Runs pytest to discover and run tests."""

    def __init__(self, verbosity=2, failfast=False, keepdb=False, **kwargs):
        self.verbosity = verbosity
        self.failfast = failfast
        self.keepdb = keepdb

    def run_tests(self, test_labels):
        """Run pytest and return the exitcode.

        It translates some of Django's test command option to pytest's.
        """
        import pytest

        argv = []
        if self.verbosity == 0:
            argv.append('--quiet')
        if self.verbosity in [1, 2]:
            argv.append('--verbose')
        if self.verbosity == 3:
            argv.append('-vv')
            argv.append('-s')
        if self.verbosity > 0:
            argv.append('--durations=0')
        if self.failfast:
            argv.append('--exitfirst')
        if self.keepdb:
            argv.append('--reuse-db')

        argv.extend(test_labels)
        return pytest.main(argv)
