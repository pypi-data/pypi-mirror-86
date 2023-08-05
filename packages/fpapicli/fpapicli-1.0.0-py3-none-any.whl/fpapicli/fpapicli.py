import click
import  requests

@click.group()
def fpapicli():
    """CLI for football player API.

    API source : http://footballplayerapi.herokuapp.com/
    """

@fpapicli.command()
def get_all():
    """ This cmd request details of all players """
    res = requests.get('http://footballplayerapi.herokuapp.com/getall')
    click.echo(res.json())

@click.option('--id',prompt="enter plr id",metavar='<int>')
@fpapicli.command(short_help='get a player details')
def get_player(id):
    """ This cmd request details of a player according to player id """
    res=requests.get('http://footballplayerapi.herokuapp.com/get/%s' %id)
    click.echo(res.json())

if __name__ == '__main__':
    fpapicli(prog_name='fpapicli')