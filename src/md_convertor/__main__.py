from md_convertor.convertor import markdown_to_pdf
import click

from md_convertor.convertor import markdown_to_html


@click.command()
@click.argument('markdown_file_path', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option('--html', '-m', is_flag=True, help='Output in html format')
@click.option('--out_dir', '-o', default=None, help='The parent dir of the output file (default: None)')
@click.option('--filename', '-n', default=None, help='The output file name (default: None)')
def main(markdown_file_path, html, out_dir, filename):
    if html:
        markdown_to_html(markdown_file_path, out_dir, filename)
    else:
        markdown_to_pdf(markdown_file_path, out_dir, filename)




if __name__ == "__main__":
    main()