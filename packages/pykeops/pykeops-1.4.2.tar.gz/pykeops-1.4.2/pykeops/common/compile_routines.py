import os
import sys
import subprocess

import pykeops.config
from pykeops.common.parse_type import check_aliases_list
from pykeops.common.utils import c_type


def run_and_display(args, build_folder, msg=''):
    """
    This function run the command stored in args and display the output if needed
    :param args: list
    :param msg: str
    :return: None
    """
    try:
        proc = subprocess.run(args, cwd=build_folder, stdout=subprocess.PIPE, check=True)
        if pykeops.config.verbose:
            print(proc.stdout.decode('utf-8'))

    except subprocess.CalledProcessError as e:
        print('\n--------------------- ' + msg + ' DEBUG -----------------')
        print(e)
        print(e.stdout.decode('utf-8'))
        print('--------------------- ----------- -----------------')


def compile_generic_routine(formula, aliases, dllname, dtype, lang, optional_flags, build_folder):
    aliases = check_aliases_list(aliases)

    def process_alias(alias):
        if alias.find("=") == -1:
            return ''  # because in this case it is not really an alias, the variable is just named
        else:
            return 'auto ' + str(alias) + '; '

    def process_disp_alias(alias):
        return str(alias) + '; '

    alias_string = ''.join([process_alias(alias) for alias in aliases])
    alias_disp_string = ''.join([process_disp_alias(alias) for alias in aliases])

    print(
        'Compiling ' + dllname + ' in ' + os.path.realpath(build_folder + os.path.sep + '..' ) + ':\n' + '       formula: ' + formula + '\n       aliases: ' + alias_disp_string + '\n       dtype  : ' + dtype + '\n... ',
        end='', flush=True)

    command_line = ["cmake", pykeops.config.script_folder,
                     "-DCMAKE_BUILD_TYPE=" + "'{}'".format(pykeops.config.build_type),
                     "-DFORMULA_OBJ=" + "'{}'".format(formula),
                     "-DVAR_ALIASES=" + "'{}'".format(alias_string),
                     "-Dshared_obj_name=" + "'{}'".format(dllname),
                     "-D__TYPE__=" + "'{}'".format(c_type[dtype]),
                     "-DPYTHON_LANG=" + "'{}'".format(lang),
                     "-DPYTHON_EXECUTABLE=" + "'{}'".format(sys.executable),
                     "-DPYBIND11_PYTHON_VERSION=" + "'{}'".format(str(sys.version_info.major) + "." + str(sys.version_info.minor)),
                     "-DC_CONTIGUOUS=1",
                    ] + optional_flags

    run_and_display(command_line + ["-DcommandLine=" + " ".join(command_line)],
                    build_folder,
                    msg="CMAKE")

    run_and_display(["cmake", "--build", ".", "--target", dllname, "--", "VERBOSE=1"], build_folder, msg="MAKE")

    print('Done.')


def compile_specific_conv_routine(dllname, dtype, build_folder):
    print('Compiling ' + dllname + ' using ' + dtype + ' in ' + os.path.realpath(build_folder + os.path.sep + '..' ) + '... ', end='', flush=True)
    run_and_display(['cmake', pykeops.config.script_folder,
                     '-DCMAKE_BUILD_TYPE=' + pykeops.config.build_type,
                     '-Ushared_obj_name',
                     '-D__TYPE__=' + c_type[dtype],
                     ],
                    build_folder,
                    msg='CMAKE')

    run_and_display(['cmake', '--build', '.', '--target', dllname, '--', 'VERBOSE=1'], build_folder, msg='MAKE')
    print('Done.')


def compile_specific_fshape_scp_routine(dllname, kernel_geom, kernel_sig, kernel_sphere, dtype, build_folder):
    print('Compiling ' + dllname + ' using ' + dtype + ' in ' + os.path.realpath(build_folder + os.path.sep + '..' ) + '... ', end='', flush=True)
    run_and_display(['cmake', pykeops.config.script_folder,
                     '-DCMAKE_BUILD_TYPE=' + pykeops.config.build_type,
                     '-Ushared_obj_name',
                     '-DKERNEL_GEOM=' + kernel_geom,
                     '-DKERNEL_SIG=' + kernel_sig,
                     '-DKERNEL_SPHERE=' + kernel_sphere,
                     '-D__TYPE__=' + c_type[dtype],
                     ],
                    build_folder,
                    msg='CMAKE')

    run_and_display(['cmake', '--build', '.', '--target', dllname, '--', 'VERBOSE=1'], build_folder, msg='MAKE')
    print('Done.')
