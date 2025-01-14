import argparse
from templater import template
from post_processor import apply_post_processes
from wikisync import sync
from converter import auto_convert

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands', dest='command')

    # Convert
    convert_parser = subparsers.add_parser("convert", help='Converts a file from .doc, .docx, or .md to .html or .md.', description='Converts a file from .doc, .docx, or .md to .html to .md.')
    convert_parser.add_argument('InFile',
                        metavar='input-file',
                        type=str,
                        help='The input path to the file that is being converted from .doc, .docx, or .md to .html and outputs that as a string.')
    convert_parser.add_argument('OutFile',
                        metavar='output-file',
                        type=str,
                        help='The output path to the file that is being converted from .doc, .docx, or .md to .html or .md and outputs that as a string.')

    # Template
    template_parser = subparsers.add_parser("template", help='Templates a source site.', description='Templates a source site.')
    template_parser.add_argument('Build',
                        metavar='output-path',
                        type=str,
                        help='The path where the templated site will be output to.')
    template_parser.add_argument('Source',
                        metavar='source-path',
                        type=str,
                        help='The path where the source site and its templates are.')

    # Post Process
    post_parser = subparsers.add_parser("post-process", help='Applies post processing to a site.', description='Applies post processing to a site.')
    post_parser.add_argument('Site',
                        metavar='site-path',
                        type=str,
                        help='The path of the site being modified.')

    post_parser.add_argument('Process',
                        metavar='process-path',
                        type=str,
                        help='The path with the following process files: ".glossary.json", ".references.json", and ".external-link-whitelist.json"')

    # Build (Template & Post Processing Combined)
    template_parser = subparsers.add_parser("build", help='Builds a source site. This combines both templating and post processing', description='Builds a source site. This combines both templating and post processing')
    template_parser.add_argument('Build',
                        metavar='output-path',
                        type=str,
                        help='The path where the templated site will be output to.')
    template_parser.add_argument('Source',
                        metavar='source-path',
                        type=str,
                        help='The path where the source site and its templates are.')

    # Sync
    sync_parser = subparsers.add_parser("sync", help='Syncs a source site with the a team\'s iGEM Wiki on the iGEM MediaWiki server.', description='Syncs a source site with the a team\'s iGEM Wiki on the iGEM MediaWiki server.')
    sync_parser.add_argument('Site',
                        metavar='site-directory',
                        type=str,
                        help='The path to the directory that is being synced to the wiki.')
    sync_parser.add_argument('Temp',
                        metavar='temp-directory',
                        type=str,
                        help='The path to a temporary directory. Used to sync the wiki.')
    sync_parser.add_argument('Team',
                        metavar='team-name',
                        type=str,
                        help='The iGEM team name.')


    args = parser.parse_args()

    if args.command == 'convert':
        input_filename = args.InFile
        output_filename = args.OutFile
        auto_convert(input_filename, output_filename)

    if args.command == 'template':
        build_path = args.Build
        source_path = args.Source
        template(build_path, source_path)

    elif args.command == 'post-process':
        build_path = args.Site
        process_path = args.Process
        apply_post_processes(build_path, process_path)

    elif args.command == 'build':
        build_path = args.Build
        source_path = args.Source
        template(build_path, source_path)
        apply_post_processes(build_path, source_path)

    elif args.command == 'sync':
        build_path = args.Site
        temp_sync_path = args.Temp
        team_name = args.Team
        sync(build_path, temp_sync_path, team_name)