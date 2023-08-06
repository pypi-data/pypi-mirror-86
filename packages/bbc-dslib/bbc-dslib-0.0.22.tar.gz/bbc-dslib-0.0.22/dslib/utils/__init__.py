from .caching import timed_cache
from .dataframe import check_size_variation, configure_pandas
from .io import ensure_directory_exists, ignore_exceptions, safe_write, read_yaml, get_tmp_dirpath, get_tmp_filepath, \
    zip_files, unzip_file
from .logging import configure_logging, log, timeit, suppress_stdout, deep_suppress_stdout_stderr
from .meta import resolve, compose
from .templating import render_file, render_string
from .temporality import midpoint_date, date_range, change_timezone, force_timezone_onto_timestamp

import importlib

package_name = 'sklearn'
spec = importlib.util.find_spec(package_name)
if spec:
    from .ml import predict_with_threshold, eval_score, eval_pipeline, FeatureSelection, load_dill_model, \
        save_dill_model
