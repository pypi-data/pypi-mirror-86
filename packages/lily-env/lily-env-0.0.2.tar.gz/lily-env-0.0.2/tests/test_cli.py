
import os
from unittest import TestCase
import textwrap

from click.testing import CliRunner
import pytest

import lily_env as env
from lily_env.cli import cli
from lily_env.parser import Env


class CliTestCase(TestCase):

    @pytest.fixture(autouse=True)
    def initfixtures(self, mocker, tmpdir):
        self.mocker = mocker
        self.tmpdir = tmpdir

    def setUp(self):
        self.runner = CliRunner()

    #
    # DUMP
    #
    def test_dump(self):

        class MyEnvParser(env.EnvParser):

            secret_key = env.CharField()

            is_important = env.BooleanField()

            aws_url = env.URLField()

            number_of_workers = env.IntegerField()

        os.environ['SECRET_KEY'] = 'secret.whatever'
        os.environ['IS_IMPORTANT'] = 'true'
        os.environ['AWS_URL'] = 'http://hello.word.org'
        os.environ['NUMBER_OF_WORKERS'] = '113'

        self.tmpdir.join('lily_env_dump.json').write('hey')
        self.mocker.patch.object(
            Env,
            'get_dump_filepath'
        ).return_value = str(self.tmpdir.join('lily_env_dump.json'))

        MyEnvParser().parse()

        result = self.runner.invoke(cli, ['dump'])

        assert result.exit_code == 0
        assert result.output.strip() == textwrap.dedent('''
            AWS_URL: http://hello.word.org
            IS_IMPORTANT: True
            NUMBER_OF_WORKERS: 113
            SECRET_KEY: secret.whatever
        ''').strip()

    def test_dump__dump_was_not_created(self):

        class MyEnvParser(env.EnvParser):

            secret_key = env.CharField()

        os.environ['SECRET_KEY'] = 'secret.whatever'

        self.mocker.patch.object(
            Env,
            'get_dump_filepath'
        ).return_value = str(self.tmpdir.join('lily_env_dump.json'))

        MyEnvParser()

        result = self.runner.invoke(cli, ['dump'])

        assert result.exit_code == 1
        assert result.output.strip() == (
            'Error: Dump file does not exist, run `parse` on your '
            '`EnvParser` instance in order to render it')
