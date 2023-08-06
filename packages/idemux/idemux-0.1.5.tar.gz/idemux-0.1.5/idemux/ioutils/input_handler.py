import gzip
import logging
import pathlib
from contextlib import ExitStack
import io
from itertools import zip_longest

log = logging.getLogger(__name__)


class FileHandlerIn(ExitStack):

    def __init__(self, mate1_path, mate2_path, memory=2 ** 30):
        self.mate1_path = pathlib.Path(mate1_path)
        self.mate2_path = pathlib.Path(mate2_path)
        self.buffer_per_file = (memory // 2)
        super().__init__()

    def __enter__(self):
        return self._get_pe_fastq(self.mate1_path, self.mate2_path)

    def _get_pe_fastq(self, fq_gz_1, fq_gz_2):
        fq_1_gz_stream = io.BufferedReader(gzip.open(self.mate1_path, 'rb'))
        fq_2_gz_stream = io.BufferedReader(gzip.open(self.mate2_path, 'rb'))
        fastq_1 = self._fastq_lines_to_reads(fq_1_gz_stream)
        fastq_2 = self._fastq_lines_to_reads(fq_2_gz_stream)
        yield zip(fastq_1, fastq_2)

    def _fastq_lines_to_reads(self, fastq_lines):
        """Collect fastq lines and chucks them into reads.
        Args:
            fastq_lines (iterable <str>): An iterable of lines from a fastq file.
        Return:
            read_iterator (iterator): All fastq lines grouped into reads (chunks of 4 lines).
        """
        # see grouper example https://docs.python.org/3/library/itertools.html
        # convert fastq lines into chunked iterator with a length of lines_per_read
        lines_per_read = 4
        chunked_lines = [iter(fastq_lines)] * lines_per_read
        # zip longest calls next when zipping the chunked iterator
        # this leads to all fastq_lines grouped by chunks of size lines_per_read
        return zip_longest(*chunked_lines)
