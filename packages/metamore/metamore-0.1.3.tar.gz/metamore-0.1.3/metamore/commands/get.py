import piexif
import click
import os


@click.command()
@click.argument('target', type=click.Path(exists=True))
@click.option('-o', '--out', is_flag=True, help='Save output to file.')
@click.option('--no-thumbnail', 'nothumb', is_flag=True, help='Ignore thumbnail data.')
def cli(target, out, nothumb):
    """Get EXIF metadata from file(s)"""
    exif_dict = piexif.load(target)

    if out:
        if nothumb:
            del exif_dict["thumbnail"]
        with open(os.path.splitext(target)[0]+'_meta.txt', 'w') as f:
            for ifd_name in exif_dict:
                print(f"\n{ifd_name}", file=f)
                for key in exif_dict[ifd_name]:
                    try:
                        print(f"\t {key}: {exif_dict[ifd_name][key][:10]}", file=f)
                    except:
                        print(f"\t {key}: {exif_dict[ifd_name][key]}", file=f)

    else:
        del exif_dict["thumbnail"]
        for ifd_name in exif_dict:
            print(f"\n{ifd_name}")
            for key in exif_dict[ifd_name]:
                try:
                    print(f"\t {key}: {exif_dict[ifd_name][key][:10]}")
                except:
                    print(f"\t {key}: {exif_dict[ifd_name][key]}")
