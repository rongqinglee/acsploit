import os
from options import Options


class File:
    """File class."""

    OUTPUT_NAME = 'file'

    def __init__(self):
        """Initialize the File class."""
        self.options = Options()
        self.options.add_option('filename', 'acsploit_output.dat', 'The name of the file to write to')
        # TODO: add more formats
        self.options.add_option('format', 'plaintext', 'The format to write output in', ['plaintext', 'csv', 'tsv', 'binary'])
        self.options.add_option('final_newline', True, 'Whether to end the file with a newline')
        self.options.add_option('number_format', 'decimal', 'Format for numbers', ['decimal', 'hexadecimal', 'octal'])

    def output(self, output_list):
        """Create file output."""
        output_path = os.path.expanduser(self.options['filename'])
        if self.options['format'] == 'binary':
            with open(output_path, 'wb') as output_file:
                self.write_binary_file(output_list, output_file)
        else:
            with open(output_path, 'w') as output_file:
                if self.options['format'] == 'plaintext':
                    self.write_plaintext_file(output_list, output_file)
                elif self.options['format'] == 'csv':
                    self.write_sv_file(output_list, output_file, ',')
                elif self.options['format'] == 'tsv':
                    self.write_sv_file(output_list, output_file, '\t')

                if self.options['final_newline']:
                    output_file.write(os.linesep)

    def write_plaintext_file(self, output_list, output_file):
        """Write plaintext payload data to output file."""
        output_file.write(os.linesep.join([self.convert_item(item) for item in output_list]))

    def write_binary_file(self, output_list, output_file):
        """Write binary payload data to output file."""
        # for a binary file, we don't want to be adding in our own lineseps
        for item in output_list:
            output_file.write(item)

    def write_sv_file(self, output_list, output_file, separator):
        """Write sv file."""
        # treat lists of lists as rows x cols
        if all(type(item) is list for item in output_list):
            # take each inner list, glue it together with the separator, then glue these together with os.linesep
            lines = [separator.join(self.convert_item(subitem) for subitem in item) for item in output_list]
            output_file.write(os.linesep.join(lines))

        else:
            output_file.write(separator.join([self.convert_item(item) for item in output_list]))

    def convert_item(self, item):
        """Convert output to hexadecimal or octal."""
        # NB: this doesn't recurse onto lists
        if type(item) is int:
            if self.options['number_format'] == 'hexadecimal':
                item = hex(item)
            elif self.options['number_format'] == 'octal':
                item = oct(item)
        return str(item)
