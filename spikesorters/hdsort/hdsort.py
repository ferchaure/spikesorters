from pathlib import Path
import os
from typing import Union
import sys
import copy

import spikeextractors as se
from ..basesorter import BaseSorter
from ..utils.shellscript import ShellScript


def check_if_installed(hdsort_path: Union[str, None]):
    if hdsort_path is None:
        return False
    assert isinstance(hdsort_path, str)

    if hdsort_path.startswith('"'):
        hdsort_path = hdsort_path[1:-1]
    hdsort_path = str(Path(hdsort_path).absolute())
    if (Path(hdsort_path) / '+hdsort').is_dir():
        return True
    else:
        return False


class HDSortSorter(BaseSorter):
    """
    """

    sorter_name: str = 'hdsort'
    hdsort_path: Union[str, None] = os.getenv('HDSORT_PATH', None)
    installed = check_if_installed(hdsort_path)
    requires_locations = False

    _default_params = {
        'detect_threshold': 4.2,
        'detect_sign': -1,  # -1 - 1
        'filter': True,
        'parfor': True,
        'hpf': 300,
        'lpf': 7000,
        'n_pc_dims': 6,
        'chunk_size': 500000,
        'loop_mode': 'local_parfor',
    }

    _extra_gui_params = [
        {'name': 'detect_threshold', 'type': 'float', 'value': 4.2, 'default': 4.2,
         'title': "Relative detection threshold"},
        {'name': 'detect_sign', 'type': 'int', 'value': -1, 'default': -1,
         'title': "Use -1, or 1, depending on the sign of the spikes in the recording"},
        {'name': 'filter', 'type': 'bool', 'value': True, 'default': True,
         'title': "If True, the recordings are filtered"},
        {'name': 'parfor', 'type': 'bool', 'value': True, 'default': True, 'title': "Use parallel processing"},
        {'name': 'hpf', 'type': 'float', 'value': 300, 'default': 300, 'title': "high-pass cutoff frequency"},
        {'name': 'lpf', 'type': 'float', 'value': 7000, 'default': 7000, 'title': "low-pass cutoff frequency"},
        {'name': 'n_pc_dims', 'type': 'int', 'value': 6, 'default': 6,
         'title': "Number of pc dimensions"},
        {'name': 'chunk_size', 'type': 'int', 'value': 500000, 'default': 500000,
         'title': "Chunk size in number of samples"},
        {'name': 'loop_mode', 'type': 'str', 'value': 'local_parfor', 'default': 'local_parfor',
         'title': "Loop mode for sorting ('local_parfor', 'loop', 'grid')"},
    ]

    _gui_params = copy.deepcopy(BaseSorter.sorter_gui_params)
    for param in _extra_gui_params:
        _gui_params.append(param)

    installation_mesg = """\nTo use HDSort run:\n
        >>> git clone https://git.bsse.ethz.ch/hima_public/HDsort.git
    and provide the installation path by setting the HDSORT_PATH
    environment variables or using HDSortSorter.set_hdsort_path().\n\n

    More information on HDSort at:
        https://git.bsse.ethz.ch/hima_public/HDsort.git
    """

    def __init__(self, **kargs):
        BaseSorter.__init__(self, **kargs)

    @staticmethod
    def get_sorter_version():
        p = os.getenv('HDSORT_PATH', None)
        if p is None:
            return 'unknown'
        else:
            with open(os.path.join(p, 'version.txt'), mode='r', encoding='utf8') as f:
                version = f.readline()
        return version

    @staticmethod
    def set_hdsort_path(hdsort_path: str):
        HDSortSorter.hdsort_path = hdsort_path
        HDSortSorter.installed = check_if_installed(HDSortSorter.hdsort_path)
        try:
            print("Setting HDSORT_PATH environment variable for subprocess calls to:", hdsort_path)
            os.environ["HDSORT_PATH"] = hdsort_path
        except Exception as e:
            print("Could not set HDSORT_PATH environment variable:", e)

    def _setup_recording(self, recording, output_folder):
        if not check_if_installed(HDSortSorter.hdsort_path):
            raise Exception(HDSortSorter.installation_mesg)
        assert isinstance(HDSortSorter.hdsort_path, str)

        source_dir = Path(__file__).parent
        utils_path = source_dir.parent / 'utils'

        # if isinstance(recording, se.Mea1kRecordingExtractor):
        #     self.params['file_name'] = str(Path(recording._file_path.absolute()))
        #     self.params['file_format'] = 'mea1k'
        # elif isinstance(recording, se.MaxOneRecordingExtractor):
        #     self.params['file_name'] = str(Path(recording._file_path.absolute()))
        #     self.params['file_format'] = 'mea1k'
        # else:
        #     file_name = output_folder / 'recording.h5'
        #     # Generate three files dataset in Mea1k format
        #     se.Mea1kRecordingExtractor.write_recording(recording=recording, save_path=str(file_name))
        #     self.params['file_name'] = str(file_name.absolute())
        #     self.params['file_format'] = 'mea1k'

        file_name = output_folder / 'recording.h5'
        # Generate three files dataset in Mea1k format
        se.Mea1kRecordingExtractor.write_recording(recording=recording, save_path=str(file_name))
        self.params['file_name'] = str(file_name.absolute())
        self.params['file_format'] = 'mea1k'

        p = self.params
        p['sort_name'] = 'hdsort_output'

        # read the template txt files
        with (source_dir / 'hdsort_master.m').open('r') as f:
            hdsort_master_txt = f.read()
        with (source_dir / 'hdsort_config.m').open('r') as f:
            hdsort_config_txt = f.read()

        # make substitutions in txt files
        hdsort_master_txt = hdsort_master_txt.format(
            hdsort_path=str(
                Path(HDSortSorter.hdsort_path).absolute()),
            utils_path=str(utils_path.absolute()),
            output_folder=str(output_folder),
            config_path=str((output_folder / 'hdsort_config.m').absolute()),
            file_name=p['file_name'],
            file_format=p['file_format'],
            sort_name=p['sort_name'],
            chunk_size=p['chunk_size'],
            loop_mode=p['loop_mode']
        )

        if p['filter']:
            p['filter'] = 1
        else:
            p['filter'] = 0

        if p['parfor']:
            p['parfor'] = 'true'
        else:
            p['parfor'] = 'false'

        hdsort_config_txt = hdsort_config_txt.format(
            filter=p['filter'],
            parfor=p['parfor'],
            hpf=p['hpf'],
            lpf=p['lpf'],
            detect_threshold=p['detect_threshold'],
            n_pc_dims=p['n_pc_dims'],
        )

        for fname, txt in zip(['hdsort_master.m', 'hdsort_config.m'],
                              [hdsort_master_txt, hdsort_config_txt]):
            with (output_folder / fname).open('w') as f:
                f.write(txt)

    def _run(self, recording, output_folder):
        tmpdir = output_folder
        os.makedirs(str(tmpdir), exist_ok=True)
        samplerate = recording.get_sampling_frequency()

        if "win" in sys.platform and sys.platform != 'darwin':
            shell_cmd = '''
                        cd {tmpdir}
                        matlab -nosplash -nodisplay -wait -r hdsort_master
                    '''.format(tmpdir=output_folder)
        else:
            shell_cmd = '''
                        #!/bin/bash
                        cd "{tmpdir}"
                        matlab -nosplash -nodisplay -r hdsort_master
                    '''.format(tmpdir=output_folder)

        shell_cmd = ShellScript(shell_cmd, keep_temp_files=True)
        shell_cmd.start()

        retcode = shell_cmd.wait()

        if retcode != 0:
            raise Exception('HDsort returned a non-zero exit code')

        samplerate_fname = str(output_folder / 'samplerate.txt')
        with open(samplerate_fname, 'w') as f:
            f.write('{}'.format(samplerate))

    @staticmethod
    def get_result_from_folder(output_folder):
        output_folder = Path(output_folder)

        result_fname = str(output_folder / 'firings.mda')
        samplerate_fname = str(output_folder / 'samplerate.txt')
        with open(samplerate_fname, 'r') as f:
            samplerate = float(f.read())
        print(samplerate)

        sorting = se.MdaSortingExtractor(file_path=result_fname, sampling_frequency=samplerate)

        return sorting
