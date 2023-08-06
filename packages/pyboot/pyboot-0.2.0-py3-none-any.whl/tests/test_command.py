from click.testing import CliRunner
from pyboot.cli import main as cli


class TestHello(object):

    def test_hello_msg(self):
        """Check if the hello command speaks to the world"""
        runner = CliRunner()
        result = runner.invoke(cli, ['speak'])
        assert result.output.strip() == 'Hello world!'

    def test_pkgdata_msg(self):
        """Check the text in the package"""
        runner = CliRunner()
        result = runner.invoke(cli, ['print'])
        assert result.output.strip() == "some text"
