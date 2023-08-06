from apio.__main__ import cli as cmd_apio


def test_apio(clirunner, validate_cliresult, configenv):
    with clirunner.isolated_filesystem():
        configenv()
        result = clirunner.invoke(cmd_apio)
        validate_cliresult(result)


def test_apio_wrong_command(clirunner, validate_cliresult, configenv):
    with clirunner.isolated_filesystem():
        configenv()
        result = clirunner.invoke(cmd_apio, ['missing_command'])
        assert result.exit_code == 2
        assert 'Error: No such command' in result.output
