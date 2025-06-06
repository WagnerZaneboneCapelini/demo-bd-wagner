"""Generate code reference pages and navigation for mkdocstrings."""

# ==============================================================================
#  Copyright (c) 2024 Federico Busetti                                         =
#  <729029+febus982@users.noreply.github.com>                                  =
#                                                                              =
#  Permission is hereby granted, free of charge, to any person obtaining a     =
#  copy of this software and associated documentation files (the "Software"),  =
#  to deal in the Software without restriction, including without limitation   =
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,    =
#  and/or sell copies of the Software, and to permit persons to whom the       =
#  Software is furnished to do so, subject to the following conditions:        =
#                                                                              =
#  The above copyright notice and this permission notice shall be included in  =
#  all copies or substantial portions of the Software.                         =
#                                                                              =
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  =
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    =
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     =
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  =
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     =
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         =
#  DEALINGS IN THE SOFTWARE.                                                   =
# ==============================================================================

#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#
# -----------------------------------------------------#
#                   Library imports                    #
# -----------------------------------------------------#
from pathlib import Path

import mkdocs_gen_files

# -----------------------------------------------------#
#                    Configuration                     #
# -----------------------------------------------------#
# Package source code relative path
src_dir = "src"
# Generated pages will be grouped in this nav folder
nav_pages_path = "MODULES-Reference"


# -----------------------------------------------------#
#                       Runner                         #
# -----------------------------------------------------#
# """ Generate code reference pages and navigation

#     Based on the recipe of mkdocstrings:
#     https://github.com/mkdocstrings/mkdocstrings
#     https://github.com/mkdocstrings/mkdocstrings/issues/389#issuecomment-1100735216

#     Credits:
#     Timothée Mazzucotelli
#     https://github.com/pawamoy
# """
# Iterate over each Python file
for path in sorted(Path(src_dir).rglob("*.py")):
    # Get path in module, documentation and absolute
    module_path = path.relative_to(src_dir).with_suffix("")
    doc_path = path.relative_to(src_dir).with_suffix(".md")
    full_doc_path = Path(nav_pages_path, doc_path)

    # Handle edge cases
    parts = (src_dir, *tuple(module_path.parts))
    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue

    # Write docstring documentation to disk via parser
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: {ident}")
    # Update parser
    mkdocs_gen_files.set_edit_path(full_doc_path, path)
