import typer
from rich.console import Console
from rich.panel import Panel

from s3_client import S3Client

app = typer.Typer()
console = Console()

@app.command()
def scan(
    profile: str = typer.Option('sapp', '--profile', '-p'),
    region: str = typer.Option('us-east-1', '--region', '-r'),
):
    console.print(Panel.fit('Iniciando escaneo', style='blue'))

    s3_client = S3Client(profile=profile, region=region)
    scan = s3_client.scan_delete_markers()
    s3_client.table_maker(scan)


@app.command()
def local_delete(
    profile: str = typer.Option('sapp', '--profile', '-p'),
    region: str = typer.Option('us-east-1', '--region', '-r'),
):
    console.print(Panel.fit('Removiendo Objetos con Delete Marker Activo Localmente', style='blue'))

    s3_client = S3Client(profile=profile, region=region)
    scan = s3_client.scan_delete_markers()
    if not scan:
        return
    for key, content in scan.items():
        content['versions'] = [value for value in content['versions'] if value.get('Type') != 'DeleteMarker']
    objetos_data = scan
    s3_client.table_maker(objetos_data)


@app.command()
def remote_delete(
    profile: str = typer.Option('sapp', '--profile', '-p'),
    region: str = typer.Option('us-east-1', '--region', '-r'),
):
    console.print(Panel.fit('Removiendo Objetos con Delete Marker Activo en BUCKET REMOTO', style='blue'))

    s3_client = S3Client(profile=profile, region=region)
    scan = s3_client.scan_delete_markers()
    delete = s3_client.remote_del(scan)
    if delete:
        console.print('[green] Eliminación exitosa') 


if __name__ == "__main__":
    app()