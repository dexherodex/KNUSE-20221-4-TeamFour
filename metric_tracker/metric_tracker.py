import io
import ast
import yaml
import json
import git
import os
import sys
import time

from metric_counter import metric_counter


class Tracker:

    def __init__(self):
        self.repository = ""
        self.target_path = ""
        self.commits = list()
        self.metric_values = dict()

    def input(self, infile):
        parse = self.parse_yaml(infile)
        self.repository = parse['repository']
        self.target_path = parse['target_path']
        for commit_hash in parse['commits']:
            self.commits.append(commit_hash)

    @staticmethod
    def parse_yaml(file_path):
        assert os.path.isfile(file_path)
        with open(file_path, 'r') as f:
            parse = yaml.safe_load(f)
            return parse

    def output(self, outfile):
        data = dict()
        data['repository'] = self.repository
        data['target_path'] = self.target_path
        data['metric_values'] = self.metric_values
        with open(outfile, "w", encoding="UTF-8") as fp:
            json.dump(data, fp, indent=4)

    def tracking(self):
        if not os.path.isdir(self.repository):
            sys.exit('ERROR: Repository %s was not found' % self.repository)

        repo = git.Repo.init(self.repository)

        for commit_hash in self.commits:
            commit = repo.commit(commit_hash)
            # self.print_info(commit)
            self.metric_values[commit_hash] = dict()
            try:
                target = commit.tree / self.target_path

                with io.BytesIO(target.data_stream.read()) as f:
                    lines = self.byte_decode(f.readlines())
                    # count number of lines if file
                    num_all_code_lines = metric_counter.count_lines_of_code(lines)
                    # count number of blanks in file
                    num_blank = metric_counter.count_blank(lines)
                    # count number of comment lines
                    num_comment, num_only_comment = metric_counter.count_comment(lines)
                    # count standalone parenthesis
                    num_standalone = metric_counter.count_standalone_paren(lines)
                f.close()

                with io.BytesIO(target.data_stream.read()) as f2:
                    ptree = ast.parse(f2.read())
                    # count number of function
                    num_function = metric_counter.count_function(ptree)
                f2.close()

                # number of lines without blanks (LOC)
                num_code_lines = num_all_code_lines - num_blank - num_only_comment
                # number of effective lines (eLOC)
                effective = num_all_code_lines - num_blank - num_only_comment - num_standalone

                self.metric_values[commit_hash]['LOC'] = str(num_code_lines)
                self.metric_values[commit_hash]['eLOC'] = str(effective)
                self.metric_values[commit_hash]['Comment'] = str(num_comment)
                self.metric_values[commit_hash]['Blank'] = str(num_blank)
                self.metric_values[commit_hash]['Nfunc'] = str(num_function)

            except KeyError:
                self.metric_values[commit_hash]['Exception'] = 'There is no target file in this commit.'

    @staticmethod
    def byte_decode(lines):
        str_lines = []
        for line in lines:
            str_lines.append(line.decode('utf-8'))
        return str_lines

    @staticmethod
    def print_info(commit):
        print("")
        print("         Commit          : ", commit)
        print("         Author          : ", commit.author, ", (",
              time.asctime(time.gmtime(commit.authored_date)), ")")
        print("         Committer       : ", commit.committer, ", (",
              time.asctime(time.gmtime(commit.committed_date)), ")")
        print("         Encoding        : ", commit.encoding)
        print("         Summary         : ", commit.summary)
        print("         Delta LOC       : ", commit.stats.total['lines'], " (+",
              commit.stats.total['insertions'], ", -",
              commit.stats.total['deletions'], ")")


def main():
    if len(sys.argv) < 3:
        print(f"Usage: <{sys.argv[0]}> <in.file> <out.file>\n")
        exit(1)

    # input file's path
    infile = sys.argv[1]

    # output file's path
    outfile = sys.argv[2]

    metric_tracker = Tracker()
    metric_tracker.input(infile)
    metric_tracker.tracking()
    metric_tracker.output(outfile)


if __name__ == '__main__':
    main()
