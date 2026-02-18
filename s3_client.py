import boto3
import typer
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from config import settings

console = Console()

class S3Client:

    def __init__(self, profile=None, region=None):
        
        try:
            self.session = boto3.Session(profile_name=profile, region_name=region)
            self.s3 = self.session.client("s3")
            self.bucket_name = settings.BUCKET_NAME

        except Exception as e:
            console.log(f'[red]Error de conexión a AWS:[/] {e}')
            raise typer.Exit(code=1)

    def scan_delete_markers(self):
        
        try:
            paginator = self.s3.get_paginator('list_object_versions')

            objetos_data = defaultdict(lambda: {'versions': [], 'tiene_delete_marker_activo': False})

            with console.status("[bold green]Escaneando versiones del bucket...") as status:
                for i, page in enumerate(paginator.paginate(Bucket=self.bucket_name)):
                    if i >= 1:
                        break
                    for versions in page.get('Versions', []):
                        key = versions['Key']
                        objetos_data[key]['versions'].append({
                            'VersionId': versions['VersionId'],
                            'StorageClass': versions['StorageClass'],
                            'Size': versions['Size'],
                            'Date': versions['LastModified'],
                            'ETag': versions['ETag'],
                            'Type': 'Version'
                        })

                    for delete_markers in page.get('DeleteMarkers', []):
                        key = delete_markers['Key']
                        if delete_markers['IsLatest']:
                            objetos_data[delete_markers['Key']]['tiene_delete_marker_activo'] = True
                        
                        objetos_data[key]['versions'].append({
                            'VersionId': delete_markers['VersionId'],
                            'Size': 0,
                            'Date': delete_markers['LastModified'],
                            'Type': 'DeleteMarker'
                        })
                    return objetos_data

        except Exception as e:
            console.log(f'[red]Error al procesar el bucket {self.bucket_name}:[/] {e}')

    def remote_del(self, data):
        
        if not data:
            return
        objetos_data = {key:value for key, value in data.items() if value.get('tiene_delete_marker_activo') == True
                        and any(versions.get('Type') == 'DeleteMarker' for versions in value.get('versions', []))}
        
        delete_batch = {
            'Objects': [ 
                {
                'Key': key,
                'VersionId': version['VersionId']
                } 
                for key, value in objetos_data.items()
                for version in value['versions']
                if version.get('Type') == 'DeleteMarker'
            ]
        }

        if delete_batch['Objects'][0]:
            console.log(f'[yellow]Procediendo a eliminar[/] {len(delete_batch['Objects'][0])} markers...')
            self.s3.delete_objects(
                Bucket=settings.BUCKET_NAME,
                Delete= {'Objects': [delete_batch['Objects'][0]]}
            )
            console.log(f'[green]Eliminados [/] {len(delete_batch['Objects'][0])} markes...')
            return True

        else:
            console.print('No se encontraron markers para eliminar')

    def table_maker(self, objetos_data: dict):

        if not objetos_data:
            return
        table = Table(title=f"Objetos con Delete Marker en: {self.bucket_name}")
        table.add_column("Key", style="cyan", no_wrap=False)
        table.add_column("Version ID", justify="center", style="magenta")
        table.add_column("Tipo", justify="center", style="yellow")
        table.add_column("Peso", justify="center")
        table.add_column("Última Modificación", style="green")
        table.add_column("Clase", style="dark_turquoise")
        
        founded = 0
        for key, info in objetos_data.items():
                if founded >= 1:
                    break
                if info['tiene_delete_marker_activo']:
                    founded += 1
                    sorted_versions = sorted(info['versions'], key=lambda x: x['Date'], reverse=True)
                    for row_data in sorted_versions:
                        size_mb = round(row_data.get('Size') / (1024 * 1024), 2)
                        table.add_row(
                            key, 
                            row_data['VersionId'],
                            row_data['Type'],
                            str(f'{size_mb} MB'),
                            row_data['Date'].strftime("%Y-%m-%d %H:%M"),
                            row_data.get('StorageClass') or 'SIN CLASE'
                        )

        if founded > 0:
            console.print(table)
            console.log(f"\n[bold green]Análisis completado.[/] Se encontraron [bold]{founded}[/] objetos con markers.")
        else:
            console.log("[yellow]No se encontraron objetos con 'Delete Marker' activo.[/]")
