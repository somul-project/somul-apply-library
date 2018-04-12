import sys

import click
import unittest as ut

from app import create_app
from app.config import Config


app = create_app(Config)


@app.cli.command(with_appcontext=False)
def unittest():
    """Run unit tests."""
    click.echo("Execute unittests.")
    tests = ut.TestLoader().discover("tests.unit", top_level_dir=".")
    test_runner = ut.runner.TextTestRunner()
    result = test_runner.run(tests)
    sys.exit(not result.wasSuccessful())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
