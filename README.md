Scripts for automatic correction
================================

Documentation is pretty bad for now, but I guess it's better to release stuff right now and maybe make it better afterwards.

Renaming directories
--------------------

Moodle puts assignments in directories having the format [group]-name_other_stuff,
with duplicates for each group member. The `rename_dirs.py` script cleans this up by
keeping one directory per group and renaming it to just the group name.

Usage: `rename_dirs.py DIRNAME`

Caution: it will remove subdirs, so don't use on directories you don't want to lose data from.

Compiling
---------

Usage: `compile_all DIRNAME FILENAME.cpp`

Will compile all instances of `DIRNAME/*/FILENAME.cpp` to `DIRNAME/*/FILENAME`.

Running tests
-------------

Test specifications format: a JSON file containing a list of dictionaries, each of which is a test case.

In the dictionaries,
 * the `input` field specifies the input to give to the program;
 * the `numeric_input` specifies an array of values that will be converted to string and fed to the program;
 * `stdout` specifies the exact output the program should print to stdout;
 * `stderr` specifies the exact output of stderr;
 * `in_stdout` specifies a substring that should be contained in stdout;
 * `close_values` specifies values that should be close to the numeric ones in the output (useful to handle floating point values)

Some example test files are included.
