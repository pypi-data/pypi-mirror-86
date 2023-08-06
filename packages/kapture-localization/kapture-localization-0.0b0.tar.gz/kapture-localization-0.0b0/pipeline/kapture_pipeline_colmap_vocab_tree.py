#!/usr/bin/env python3
# Copyright 2020-present NAVER Corp. Under BSD 3-clause license

"""
This script builds a COLMAP model (map) from kapture format (images, cameras, trajectories) with colmap sift+vocab tree
"""

import argparse
import logging
import os
import os.path as path
from typing import List, Optional

import pipeline_import_paths  # noqa: F401
import kapture_localization.utils.logging
from kapture_localization.utils.symlink import can_use_symlinks
from kapture_localization.utils.subprocess import run_python_command
from kapture_localization.colmap.colmap_command import CONFIGS

import kapture_localization.utils.path_to_kapture  # noqa: F401
import kapture.utils.logging

logger = logging.getLogger('colmap_vocab_tree_pipeline')


def colmap_vocab_tree_pipeline(kapture_map_path: str,
                               kapture_query_path: Optional[str],
                               colmap_map_path: Optional[str],
                               localization_output_path: str,
                               colmap_binary: str,
                               vocab_tree_path: str,
                               config: int,
                               prepend_cam: bool,
                               bins_as_str: List[str],
                               skip_list: List[str],
                               force_overwrite_existing: bool) -> None:
    """
    Build a colmap model using sift features and vocab tree matching features with the kapture data.

    :param kapture_map_path: path to the kapture map directory
    :type kapture_map_path: str
    :param kapture_query_path: path to the kapture query directory
    :type kapture_query_path: Optional[str]
    :param colmap_map_path: input path to the colmap reconstruction folder
    :type colmap_map_path: Optional[str]
    :param localization_output_path: output path to the localization results
    :type localization_output_path: str
    :param colmap_binary: path to the colmap executable
    :type colmap_binary: str
    :param vocab_tree_path: full path to Vocabulary Tree file used for matching
    :type vocab_tree_path: str
    :param config: index of the config parameters to use for image registrator
    :type config: int
    :param prepend_cam: prepend camera names to filename in LTVL2020 formatted output
    :type prepend_cam: bool
    :param bins_as_str: list of bin names
    :type bins_as_str: List[str]
    :param skip_list: list of steps to ignore
    :type skip_list: List[str]
    :param force_overwrite_existing: silently overwrite files if already exists
    :type force_overwrite_existing: bool
    """
    if colmap_map_path is None:
        colmap_map_path = path.join(localization_output_path, 'colmap_map')
        os.makedirs(colmap_map_path, exist_ok=True)
    elif 'colmap_build_sift_map' not in skip_list:
        logger.info('--colmap-map is not None, reusing existing map, skipping colmap_build_sift_map')
        skip_list.append('colmap_build_sift_map')

    # kapture_colmap_build_sift_map.py
    if 'colmap_build_sift_map' not in skip_list:
        local_build_sift_map_path = path.join(pipeline_import_paths.HERE_PATH,
                                              '../tools/kapture_colmap_build_sift_map.py')

        build_sift_map_args = ['-v', str(logger.level),
                               '-i', kapture_map_path,
                               '-o', colmap_map_path,
                               '-voc', vocab_tree_path,
                               '-colmap', colmap_binary]
        if force_overwrite_existing:
            build_sift_map_args.append('-f')
        build_sift_map_args += ['--Mapper.ba_refine_focal_length', '0',
                                '--Mapper.ba_refine_principal_point', '0',
                                '--Mapper.ba_refine_extra_params', '0']
        run_python_command(local_build_sift_map_path, build_sift_map_args)

    if kapture_query_path is None:
        return

    colmap_localize_path = path.join(localization_output_path, f'colmap_localized')
    os.makedirs(colmap_localize_path, exist_ok=True)
    kapture_localize_import_path = path.join(localization_output_path, f'kapture_localized')
    eval_path = path.join(localization_output_path, f'eval')
    LTVL2020_output_path = path.join(localization_output_path, 'LTVL2020_style_result.txt')

    # kapture_colmap_localize_sift.py
    if 'colmap_localize_sift' not in skip_list:
        local_localize_sift_path = path.join(pipeline_import_paths.HERE_PATH,
                                             '../tools/kapture_colmap_localize_sift.py')
        localize_sift_args = ['-v', str(logger.level),
                              '-i', kapture_query_path,
                              '-db', path.join(colmap_map_path, 'colmap.db'),
                              '-txt', path.join(colmap_map_path, 'reconstruction'),
                              '-o', colmap_localize_path,
                              '-voc', vocab_tree_path,
                              '-colmap', colmap_binary]
        if force_overwrite_existing:
            localize_sift_args.append('-f')
        localize_sift_args += CONFIGS[config]
        run_python_command(local_localize_sift_path, localize_sift_args)

    # kapture_import_colmap.py
    if 'import_colmap' not in skip_list:
        local_import_colmap_path = path.join(pipeline_import_paths.HERE_PATH,
                                             '../../kapture/tools/kapture_import_colmap.py')
        import_colmap_args = ['-v', str(logger.level),
                              '-db', path.join(colmap_localize_path, 'colmap.db'),
                              '-txt', path.join(colmap_localize_path, 'reconstruction'),
                              '-o', kapture_localize_import_path,
                              '--skip_reconstruction']
        if force_overwrite_existing:
            import_colmap_args.append('-f')
        run_python_command(local_import_colmap_path, import_colmap_args)

    # kapture_evaluate.py
    if 'evaluate' not in skip_list and path.isfile(path.join(kapture_query_path, 'sensors/trajectories.txt')):
        local_evaluate_path = path.join(pipeline_import_paths.HERE_PATH, '../tools/kapture_evaluate.py')
        evaluate_args = ['-v', str(logger.level),
                         '-i', kapture_localize_import_path,
                         '--labels', f'sift_colmap_vocab_tree_config_{config}',
                         '-gt', kapture_query_path,
                         '-o', eval_path]
        evaluate_args += ['--bins'] + bins_as_str
        if force_overwrite_existing:
            evaluate_args.append('-f')
        run_python_command(local_evaluate_path, evaluate_args)

    # kapture_export_LTVL2020.py
    if 'export_LTVL2020' not in skip_list:
        local_export_LTVL2020_path = path.join(pipeline_import_paths.HERE_PATH,
                                               '../../kapture/tools/kapture_export_LTVL2020.py')
        export_LTVL2020_args = ['-v', str(logger.level),
                                '-i', kapture_localize_import_path,
                                '-o', LTVL2020_output_path]
        if prepend_cam:
            export_LTVL2020_args.append('-p')
        if force_overwrite_existing:
            export_LTVL2020_args.append('-f')
        run_python_command(local_export_LTVL2020_path, export_LTVL2020_args)


def colmap_vocab_tree_pipeline_command_line():
    """
    Parse the command line arguments to build a map and localize images using colmap on the given kapture data.
    """
    parser = argparse.ArgumentParser(description='localize images given in kapture format on a colmap map')
    parser_verbosity = parser.add_mutually_exclusive_group()
    parser_verbosity.add_argument('-v', '--verbose', nargs='?', default=logging.WARNING, const=logging.INFO,
                                  action=kapture.utils.logging.VerbosityParser,
                                  help='verbosity level (debug, info, warning, critical, ... or int value) [warning]')
    parser_verbosity.add_argument('-q', '--silent', '--quiet', action='store_const',
                                  dest='verbose', const=logging.CRITICAL)
    parser.add_argument('-f', '-y', '--force', action='store_true', default=False,
                        help='silently delete pairfile and localization results if already exists.')
    parser.add_argument('-i', '--kapture-map', required=True,
                        help='path to the kapture map directory')
    parser.add_argument('--query', default=None,
                        help='input path to kapture mapping data root directory')
    parser.add_argument('--colmap-map', default=None,
                        help='path to the input colmap map directory (will be computed when left to None)')
    parser.add_argument('-o', '--output', required=True,
                        help='output directory.')
    parser.add_argument('-colmap', '--colmap_binary', required=False,
                        default="colmap",
                        help='full path to colmap binary '
                             '(default is "colmap", i.e. assume the binary'
                             ' is in the user PATH).')
    parser.add_argument('-voc', '--vocab_tree_path', required=True,
                        help='full path to Vocabulary Tree file'
                             ' used for matching.')
    parser.add_argument('--config', default=1, type=int,
                        choices=list(range(len(CONFIGS))), help='what config to use for image registrator')
    parser.add_argument('--prepend_cam', action='store_true', default=False,
                        help=('prepend camera names to filename in LTVL2020 formatted output. '
                              'Toggle this only for RobotCar_Seasons and RobotCar Seasons v2'))
    parser.add_argument('--bins', nargs='+', default=["0.25 2", "0.5 5", "5 10"],
                        help='the desired positions/rotations thresholds for bins'
                        'format is string : position_threshold_in_m space rotation_threshold_in_degree')
    parser.add_argument('-s', '--skip', choices=['colmap_build_sift_map'
                                                 'colmap_localize_sift.py',
                                                 'import_colmap',
                                                 'evaluate',
                                                 'export_LTVL2020'],
                        nargs='+', default=[],
                        help='steps to skip')
    args = parser.parse_args()

    logger.setLevel(args.verbose)
    if args.verbose <= logging.INFO:
        # also let kapture express its logs
        kapture.utils.logging.getLogger().setLevel(args.verbose)
        kapture_localization.utils.logging.getLogger().setLevel(args.verbose)

    args_dict = vars(args)
    logger.debug('localize.py \\\n' + '  \\\n'.join(
        '--{:20} {:100}'.format(k, str(v)) for k, v in args_dict.items()))
    if can_use_symlinks():
        colmap_vocab_tree_pipeline(args.kapture_map,
                                   args.query,
                                   args.colmap_map,
                                   args.output,
                                   args.colmap_binary,
                                   args.vocab_tree_path,
                                   args.config,
                                   args.prepend_cam,
                                   args.bins,
                                   args.skip,
                                   args.force)
    else:
        raise EnvironmentError('Please restart this command as admin, it is required for os.symlink'
                               'see https://docs.python.org/3.6/library/os.html#os.symlink')
        # need to find a way to redirect output, else it closes on error...
        # logger.critical('Request UAC for symlink rights...')
        # ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


if __name__ == '__main__':
    colmap_vocab_tree_pipeline_command_line()
