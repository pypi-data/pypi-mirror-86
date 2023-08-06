#!/usr/bin/env python

"""Tests for `fibonacci_mpu` package."""


import unittest
from click.testing import CliRunner

from fibonacci_mpu import fibonacci_mpu
from fibonacci_mpu import cli


class TestFibonacci_mpu(unittest.TestCase):
    """Tests for `fibonacci_mpu` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'fibonacci_mpu.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
