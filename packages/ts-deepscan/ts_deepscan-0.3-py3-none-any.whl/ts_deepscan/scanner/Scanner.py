import os
import threading
import logging

from .. import config

from queue import *
from pathlib import Path

from ..analyser.FileAnalyser import *
from .ScanException import *


class Scanner(object):
    __version = "0.2"

    def __init__(self, analysers, options: AnalyserOptions=None, *args, **kwargs):
        self.__analysers = analysers
        self.options = options

        self.lock = threading.Lock()

        # Result callbacks
        self.onFileScanSuccess = None # Lambda accepting dict with results
        self.onFileScanError = None # Lambda accepting path of the file and the error

        # File size limit
        self.__file_size_limit = config.get_scan_max_size()


    @property
    def totalTasks(self) -> int:
        raise NotImplementedError()

    @property
    def finishedTasks(self) -> int:
        raise NotImplementedError()

    def run(self):
        logging.info('Scanner version: {}'.format(Scanner.__version))

        try:
            return self.run_impl()

        except ScanException as err:
            logging.error(err)
            raise

        except:
            logging.exception('Internal error')
            raise InternalScanException


    def run_impl(self):
        raise NotImplementedError()


    def scan_file(self, path: Path):
        if path.is_file() and path.stat().st_size > self.__file_size_limit:
            return {}

        analysers = [a for a in self.__analysers if a.accepts(path, self.options)]
        return self.perform_scan_using(path, analysers)


    def perform_scan_using(self, path: Path, analysers):
        result = {}

        for analyse in analysers:
            res = analyse(path, self.options)
            if res:
                result[analyse.category_name] = res

        return result



class FileScanner(Scanner):
    def __init__(self, path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = path
        self.__finished = False

    @property
    def totalTasks(self) -> int:
        return 1

    @property
    def finishedTasks(self) -> int:
        with self.lock:
            return 1 if self.__finished else 0


    def run_impl(self):
        try:
            result = self.scan_file(self.path)
            if result:
                result = { self.path.name: result }

            with self.lock:
                self.__finished = True

            if self.onFileScanSuccess:
                self.onFileScanSuccess(result)
                return None
            else:
                return result

        except:
            if self.onFileScanError:
                self.onFileScanError(self.path.name)
                return None
            else:
                return None



class FolderScanner(Scanner):
    def __init__(self, path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = path
        self.__tasks = Queue()
        self.__parallel_tasks = None # os.cpu_count()

        # TODO: implement using multiprocessing
        if not self.__parallel_tasks:
            self.__parallel_tasks = 1
        else:
            self.__parallel_tasks = max(1, int(self.__parallel_tasks / 2))

        logging.info('Num of parallel jobs: {}'.format(self.__parallel_tasks))

        self.__totalTasks = 0


    @property
    def tasks(self):
        return self.__tasks

    @property
    def totalTasks(self) -> int:
        with self.lock:
            return self.__totalTasks

    @property
    def finishedTasks(self) -> int:
        with self.lock:
            return self.__totalTasks - self.__tasks.qsize()

    def run_impl(self):
        workers = [Worker(self) for _ in range(self.__parallel_tasks)]

        for w in workers:
            w.start()

        for root, dirs, files in os.walk(str(self.path)):
            dirs[:] = [d for d in dirs if not d.startswith('.git')]
            for file in files:
                if not file.startswith('.'):
                    with self.lock:
                        self.__totalTasks += 1
                    self.__tasks.put(Path(os.path.join(root, file)))

        for _ in workers:
            self.__tasks.put(None)

        files = {}
        for w in workers:
            files.update(w.results)

        return files



class Worker(threading.Thread):
    def __init__(self, scanner):
        threading.Thread.__init__(self)

        self.__scanner = scanner
        self.__results = {}


    @property
    def results(self):
        self.join()
        return self.__results


    def run(self):
        while True:
            path = self.__scanner.tasks.get()
            if path is None:
                break

            relpath = str(path.relative_to(self.__scanner.path))

            try:
                result = self.__scanner.scan_file(path)

                if not result:
                    continue

                result = {relpath: result}

                if self.__scanner.onFileScanSuccess:
                    self.__scanner.onFileScanSuccess(result)
                else:
                    self.__results.update(result)

            except Exception as err:
                if self.__scanner.onFileScanError:
                    self.__scanner.onFileScanError(relpath, err)

            except:
                logging.exception("Error occured while scanning %s.", relpath)
                if self.__scanner.onFileScanError:
                    self.__scanner.onFileScanError(relpath, None)





