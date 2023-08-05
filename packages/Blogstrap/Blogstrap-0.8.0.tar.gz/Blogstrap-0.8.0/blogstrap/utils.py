# Copyright 2020 Joe H. Rahme <joehakimrahme@gmail.com>
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import re


# We define a _builder function so that the regex is compiled only
# once. I don't know if it's necessary but it's elegant.
def parse_metadata_builder():
    pattern = re.compile(r'^\s*#\s*(?P<key>[^: ]+)\s*:\s*(?P<value>.+)')

    def _parser(article):
        lines = article.split("\n")
        metadata = {}
        for lino, line in enumerate(lines):
            # Leading and trailing whitespaces can be ignored.
            line = line.strip()
            if line == '':
                continue
            if not line.startswith('#'):
                break
            m = pattern.match(line)
            # if a metadata is malformed, it breaks the parsing and marks
            # the remainder as the content.
            if not m:
                break
            metadata[m.group('key')] = m.group('value')
        body = "\n".join(lines[lino:])

        return {'metadata': metadata,
                'content': body}
    return _parser


parse_metadata = parse_metadata_builder()
