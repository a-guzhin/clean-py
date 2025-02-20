import argparse
import glob
import logging
from pathlib import Path

from .clean_py import clean_ipynb, clean_py

logging.basicConfig(level=logging.INFO)


def str_to_bool(value):
    if value.lower() in {'false', 'f', '0', 'no', 'n'}:
        return False
    elif value.lower() in {'true', 't', '1', 'yes', 'y'}:
        return True
    raise ValueError(f'{value} is not a valid boolean value')


parser = argparse.ArgumentParser(
    prog="clean_py",
    description="Auto-lint .py and .ipynb files with autoflake, isort and black",
)
parser.add_argument("path", nargs='+', type=str, help="Files or dirs to clean")
parser.add_argument("--py", type=str_to_bool, default=True, required=False, help="Apply to .py source")
parser.add_argument("--ipynb", type=str_to_bool, default=True, help="Apply to .ipynb source")
parser.add_argument("--autoflake", type=str_to_bool, default=True, help="Apply autoflake to source")
parser.add_argument("--isort", type=str_to_bool, default=True, help="Apply isort to source")
parser.add_argument("--black", type=str_to_bool, default=True, help="Apply black to source")
args = parser.parse_args()


def main():
    for _path in args.path:
        path = Path(_path)
        if not path.exists():
            raise ValueError("Provide a valid path to a file or directory")

        if path.is_dir():
            # recursively apply to all .py source within dir
            logging.info(f"Recursively cleaning directory: {path}")
            if args.py:
                for e in glob.iglob(f"{path.as_posix()}/**/*.py", recursive=True):
                    try:
                        logging.info(f"Cleaning file: {e}")
                        clean_py(
                            py_file_path=e,
                            autoflake=args.autoflake,
                            isort=args.isort,
                            black=args.black
                        )
                    except Exception:
                        logging.error(f"Unable to clean file: {e}")
            if args.ipynb:
                # recursively apply to all .ipynb source within dir
                for e in glob.iglob(f"{path.as_posix()}/**/*.ipynb", recursive=True):
                    try:
                        logging.info(f"Cleaning file: {e}")
                        clean_ipynb(
                            ipynb_file_path=e,
                            clear_output=True,
                            autoflake=args.autoflake,
                            isort=args.isort,
                            black=args.black
                        )
                    except Exception:
                        logging.error(f"Unable to clean file: {e}")

        if path.is_file():
            if args.py and path.suffix == ".py":
                try:
                    logging.info(f"Cleaning file: {path}")
                    clean_py(
                        py_file_path=path,
                        autoflake=args.autoflake,
                        isort=args.isort,
                        black=args.black
                    )
                except Exception:
                    logging.error(f"Unable to clean file: {path}")

            elif args.ipynb and path.suffix == ".ipynb":
                try:
                    logging.info(f"Cleaning file: {path}")
                    clean_ipynb(
                        ipynb_file_path=path,
                        clear_output=True,
                        autoflake=args.autoflake,
                        isort=args.isort,
                        black=args.black
                    )
                except Exception:
                    logging.error(f"Unable to clean file: {path}")

            else:
                raise ValueError(f"Unable to clean {path} with args! Double check your args..")
