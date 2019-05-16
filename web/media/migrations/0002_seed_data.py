# Generated by Django 2.1.7 on 2019-04-03 18:38

from django.db import migrations

def create_source_kinds(apps, schema_editor):
    kinds = [
        {
            'name': 'reddit-saves',
            'description': 'A reddit account with saved posts to download.'
        },
        {
            'name': 'imgur',
            'description': 'An imgur album or direct image link to download.'
        },
        {
            'name': 'file-system',
            'description': 'A path to a local directory to import.'
        },
        {
            'name': 'reddit-post',
            'description': 'An image, album, or comment on reddit.'
        },
        {
            'name': 'ripme',
            'description': 'URL to be handled by download utility.'
        }
    ]

    SourceKind = apps.get_model('media', 'SourceKind')
    for kind in kinds:
        SourceKind.objects.create(
            name=kind['name'],
            description=kind['description']
        )

def create_storage_kinds(apps, schema_editor):
    kinds = [
        {
            'name': 'ecryptfs',
            'description': 'Encrypted file system requiring a password.',
            'mount_script_path': '<script>/ecryptfs/mount.sh',
            'unmount_script_path': '<script>/ecryptfs/unmount.sh'
        }
    ]

    StorageKind = apps.get_model('media', 'StorageKind')
    for kind in kinds:
        StorageKind.objects.create(
            name=kind['name'],
            description=kind['description'],
            mount_script_path=kind['mount_script_path'],
            unmount_script_path=kind['unmount_script_path']
        )

def create_job_statuses(apps, schema_editor):
        kinds = [
            {
                'name': 'pending',
                'description': 'The job is scheduled to run.'
            },
            {
                'name': 'failed',
                'description': 'An error occurred that caused the job the prematurely exit.'
            },
            {
                'name': 'success',
                'description': 'The job finished running without error.'
            },
            {
                'name': 'running',
                'description': 'The job was acquired by a worker.'
            }
        ]

        JobStatus = apps.get_model('media', 'JobStatus')
        for kind in kinds:
            JobStatus.objects.create(
                name=kind['name'],
                description=kind['description']
            )

class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_source_kinds),
        migrations.RunPython(create_storage_kinds),
        migrations.RunPython(create_job_statuses),
    ]
