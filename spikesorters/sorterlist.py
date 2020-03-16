from .hdsort import HDSortSorter
from .klusta import KlustaSorter
from .tridesclous import TridesclousSorter
from .mountainsort4 import Mountainsort4Sorter
from .ironclust import IronClustSorter
from .kilosort import KilosortSorter
from .kilosort2 import Kilosort2Sorter
from .spyking_circus import SpykingcircusSorter
from .herdingspikes import HerdingspikesSorter
from .waveclus import WaveClusSorter

sorter_full_list = [
    HDSortSorter,
    KlustaSorter,
    TridesclousSorter,
    Mountainsort4Sorter,
    IronClustSorter,
    KilosortSorter,
    Kilosort2Sorter,
    SpykingcircusSorter,
    HerdingspikesSorter,
    WaveClusSorter
]

sorter_dict = {s.sorter_name: s for s in sorter_full_list}

installed_sorter_list = [s for s in sorter_full_list if s.installed]


# generic laucnher via function approach
def run_sorter(sorter_name_or_class, recording, output_folder=None, delete_output_folder=False,
               grouping_property=None, parallel=False, verbose=False, **params):
    """
    Generic function to run a sorter via function approach.

    Two usages with name or class:

    by name:
       >>> sorting = run_sorter('tridesclous', recording)

    by class:
       >>> sorting = run_sorter(TridesclousSorter, recording)

    Parameters
    ----------
    sorter_name_or_class: str or SorterClass
        The sorter to retrieve default parameters from
    recording: RecordingExtractor
        The recording extractor to be spike sorted
    output_folder: str or Path
        Path to output folder
    delete_output_folder: bool
        If True, output folder is deleted (default False)
    grouping_property: str
        Splits spike sorting by 'grouping_property' (e.g. 'groups')
    parallel: bool
        If True and spike sorting is by 'grouping_property', spike sorting jobs are launched in parallel
    verbose: bool
        If True, output is verbose
    **params: keyword args
        Spike sorter specific arguments (they can be retrieved with 'get_default_params(sorter_name_or_class)'

    Returns
    -------
    sortingextractor: SortingExtractor
        The spike sorted data

    """
    if isinstance(sorter_name_or_class, str):
        SorterClass = sorter_dict[sorter_name_or_class]
    elif sorter_name_or_class in sorter_full_list:
        SorterClass = sorter_name_or_class
    else:
        raise (ValueError('Unknown sorter'))

    sorter = SorterClass(recording=recording, output_folder=output_folder, grouping_property=grouping_property,
                         parallel=parallel, verbose=verbose, delete_output_folder=delete_output_folder)
    sorter.set_params(**params)
    sorter.run()
    sortingextractor = sorter.get_result()

    return sortingextractor


def available_sorters():
    '''
    Lists available sorters.
    '''
    return sorted(list(sorter_dict.keys()))


def installed_sorters():
    '''
    Lists installed sorters.
    '''
    return sorted(list([s.sorter_name for s in installed_sorter_list]))

def print_sorter_versions():
    txt = ''
    for name in installed_sorters():
        version = sorter_dict[name].get_sorter_version()
        txt += '{}: {}\n'.format(name, version)
    txt = txt[:-1]
    print(txt)
    

def get_default_params(sorter_name_or_class):
    '''
    Returns default parameters for the specified sorter.

    Parameters
    ----------
    sorter_name_or_class: str or SorterClass
        The sorter to retrieve default parameters from

    Returns
    -------
    default_params: dict
        Dictionary with default params for the specified sorter

    '''
    if isinstance(sorter_name_or_class, str):
        SorterClass = sorter_dict[sorter_name_or_class]
    elif sorter_name_or_class in sorter_full_list:
        SorterClass = sorter_name_or_class
    else:
        raise (ValueError('Unknown sorter'))

    return SorterClass.default_params()


def run_hdsort(*args, **kwargs):
    """
    Runs HDsort sorter

    Parameters
    ----------
    *args: arguments of 'run_sorter'
        recording: RecordingExtractor
            The recording extractor to be spike sorted
        output_folder: str or Path
            Path to output folder
        delete_output_folder: bool
            If True, output folder is deleted (default False)
        grouping_property: str
            Splits spike sorting by 'grouping_property' (e.g. 'groups')
        parallel: bool
            If True and spike sorting is by 'grouping_property', spike sorting jobs are launched in parallel
        verbose: bool
            If True, output is verbose
    **kwargs: keyword args
        Spike sorter specific arguments (they can be retrieved with 'get_default_params('hdsort')

    Returns
    -------
    sortingextractor: SortingExtractor
        The spike sorted data
    """
    return run_sorter('hdsort', *args, **kwargs)


def run_klusta(*args, **kwargs):
    """
    Runs klusta sorter

    Parameters
    ----------
    *args: arguments of 'run_sorter'
        recording: RecordingExtractor
            The recording extractor to be spike sorted
        output_folder: str or Path
            Path to output folder
        delete_output_folder: bool
            If True, output folder is deleted (default False)
        grouping_property: str
            Splits spike sorting by 'grouping_property' (e.g. 'groups')
        parallel: bool
            If True and spike sorting is by 'grouping_property', spike sorting jobs are launched in parallel
        verbose: bool
            If True, output is verbose
    **kwargs: keyword args
        Spike sorter specific arguments (they can be retrieved with 'get_default_params('klusta')

    Returns
    -------
    sortingextractor: SortingExtractor
        The spike sorted data
    """
    return run_sorter('klusta', *args, **kwargs)


def run_tridesclous(*args, **kwargs):
    """
    Runs tridesclous sorter

    Parameters
    ----------
    *args: arguments of 'run_sorter'
        recording: RecordingExtractor
            The recording extractor to be spike sorted
        output_folder: str or Path
            Path to output folder
        delete_output_folder: bool
            If True, output folder is deleted (default False)
        grouping_property: str
            Splits spike sorting by 'grouping_property' (e.g. 'groups')
        parallel: bool
            If True and spike sorting is by 'grouping_property', spike sorting jobs are launched in parallel
        verbose: bool
            If True, output is verbose
    **kwargs: keyword args
        Spike sorter specific arguments (they can be retrieved with 'get_default_params('tridesclous')

    Returns
    -------
    sortingextractor: SortingExtractor
        The spike sorted data
    """
    return run_sorter('tridesclous', *args, **kwargs)


def run_mountainsort4(*args, **kwargs):
    """
    Runs mountainsort4 sorter

    Parameters
    ----------
    *args: arguments of 'run_sorter'
        recording: RecordingExtractor
            The recording extractor to be spike sorted
        output_folder: str or Path
            Path to output folder
        delete_output_folder: bool
            If True, output folder is deleted (default False)
        grouping_property: str
            Splits spike sorting by 'grouping_property' (e.g. 'groups')
        parallel: bool
            If True and spike sorting is by 'grouping_property', spike sorting jobs are launched in parallel
        verbose: bool
            If True, output is verbose
    **kwargs: keyword args
        Spike sorter specific arguments (they can be retrieved with 'get_default_params('mountainsort4')

    Returns
    -------
    sortingextractor: SortingExtractor
        The spike sorted data
    """
    return run_sorter('mountainsort4', *args, **kwargs)


def run_ironclust(*args, **kwargs):
    """
    Runs ironclust sorter

    Parameters
    ----------
    *args: arguments of 'run_sorter'
        recording: RecordingExtractor
            The recording extractor to be spike sorted
        output_folder: str or Path
            Path to output folder
        delete_output_folder: bool
            If True, output folder is deleted (default False)
        grouping_property: str
            Splits spike sorting by 'grouping_property' (e.g. 'groups')
        parallel: bool
            If True and spike sorting is by 'grouping_property', spike sorting jobs are launched in parallel
        verbose: bool
            If True, output is verbose
    **kwargs: keyword args
        Spike sorter specific arguments (they can be retrieved with 'get_default_params('ironclust')

    Returns
    -------
    sortingextractor: SortingExtractor
        The spike sorted data
    """
    return run_sorter('ironclust', *args, **kwargs)


def run_kilosort(*args, **kwargs):
    """
    Runs kilosort sorter

    Parameters
    ----------
    *args: arguments of 'run_sorter'
        recording: RecordingExtractor
            The recording extractor to be spike sorted
        output_folder: str or Path
            Path to output folder
        delete_output_folder: bool
            If True, output folder is deleted (default False)
        grouping_property: str
            Splits spike sorting by 'grouping_property' (e.g. 'groups')
        parallel: bool
            If True and spike sorting is by 'grouping_property', spike sorting jobs are launched in parallel
        verbose: bool
            If True, output is verbose
    **kwargs: keyword args
        Spike sorter specific arguments (they can be retrieved with 'get_default_params('kilosort')

    Returns
    -------
    sortingextractor: SortingExtractor
        The spike sorted data
    """
    return run_sorter('kilosort', *args, **kwargs)


def run_kilosort2(*args, **kwargs):
    """
    Runs kilosort2 sorter

    Parameters
    ----------
    *args: arguments of 'run_sorter'
        recording: RecordingExtractor
            The recording extractor to be spike sorted
        output_folder: str or Path
            Path to output folder
        delete_output_folder: bool
            If True, output folder is deleted (default False)
        grouping_property: str
            Splits spike sorting by 'grouping_property' (e.g. 'groups')
        parallel: bool
            If True and spike sorting is by 'grouping_property', spike sorting jobs are launched in parallel
        verbose: bool
            If True, output is verbose
    **kwargs: keyword args
        Spike sorter specific arguments (they can be retrieved with 'get_default_params('kilosort2')

    Returns
    -------
    sortingextractor: SortingExtractor
        The spike sorted data
    """
    return run_sorter('kilosort2', *args, **kwargs)


def run_spykingcircus(*args, **kwargs):
    """
    Runs spykingcircus sorter

    Parameters
    ----------
    *args: arguments of 'run_sorter'
        recording: RecordingExtractor
            The recording extractor to be spike sorted
        output_folder: str or Path
            Path to output folder
        delete_output_folder: bool
            If True, output folder is deleted (default False)
        grouping_property: str
            Splits spike sorting by 'grouping_property' (e.g. 'groups')
        parallel: bool
            If True and spike sorting is by 'grouping_property', spike sorting jobs are launched in parallel
        verbose: bool
            If True, output is verbose
    **kwargs: keyword args
        Spike sorter specific arguments (they can be retrieved with 'get_default_params('spykingcircus')

    Returns
    -------
    sortingextractor: SortingExtractor
        The spike sorted data
    """
    return run_sorter('spykingcircus', *args, **kwargs)


def run_herdingspikes(*args, **kwargs):
    """
    Runs herdingspikes sorter

    Parameters
    ----------
    *args: arguments of 'run_sorter'
        recording: RecordingExtractor
            The recording extractor to be spike sorted
        output_folder: str or Path
            Path to output folder
        delete_output_folder: bool
            If True, output folder is deleted (default False)
        grouping_property: str
            Splits spike sorting by 'grouping_property' (e.g. 'groups')
        parallel: bool
            If True and spike sorting is by 'grouping_property', spike sorting jobs are launched in parallel
        verbose: bool
            If True, output is verbose
    **kwargs: keyword args
        Spike sorter specific arguments (they can be retrieved with 'get_default_params('herdingspikes')

    Returns
    -------
    sortingextractor: SortingExtractor
        The spike sorted data
    """
    return run_sorter('herdingspikes', *args, **kwargs)


def run_waveclus(*args, **kwargs):
    """
    Runs waveclus sorter

    Parameters
    ----------
    *args: arguments of 'run_sorter'
        recording: RecordingExtractor
            The recording extractor to be spike sorted
        output_folder: str or Path
            Path to output folder
        delete_output_folder: bool
            If True, output folder is deleted (default False)
        grouping_property: str
            Splits spike sorting by 'grouping_property' (e.g. 'groups')
        parallel: bool
            If True and spike sorting is by 'grouping_property', spike sorting jobs are launched in parallel
        verbose: bool
            If True, output is verbose
    **kwargs: keyword args
        Spike sorter specific arguments (they can be retrieved with 'get_default_params('waveclus')

    Returns
    -------
    sortingextractor: SortingExtractor
        The spike sorted data
    """
    return run_sorter('waveclus', *args, **kwargs)
