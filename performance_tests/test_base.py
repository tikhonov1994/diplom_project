from abc import ABC, abstractmethod
import multiprocessing as mp


class TestBase(ABC):
    READ_QUERY = ''

    @abstractmethod
    def test_read(self, n: int = 10) -> dict[str, any]:
        raise NotImplementedError

    @abstractmethod
    def test_write(self, chunk_file: str, n: int = 10) -> dict[str, any]:
        raise NotImplementedError

    def _work(self, kind: str, chunk_f: str, iter_count: int) -> dict[str, any]:
        if kind == 'read':
            return self.test_read(iter_count)
        elif kind == 'write':
            return self.test_write(chunk_f, iter_count)
        else:
            raise ValueError

    def test_read_mp(self, cores: int = 4, n: int = 10) -> dict[str, any]:
        with mp.Pool(cores) as pool:
            results = pool.map(self.test_read, [n for _ in range(cores)])
            avg_seconds = sum([test['test_read']['avg_seconds'] for test in results]) / len(results)
            return {'test_read_mp': {
                'operation': self.READ_QUERY,
                'cores': cores,
                'iterations': n,
                'avg_seconds': avg_seconds
            }}

    def test_write_mp(self, chunk_file: str, cores: int = 4, n: int = 4) -> dict[str, any]:
        with mp.Pool(cores) as pool:
            results = pool.starmap(self.test_write, [(chunk_file, n) for _ in range(cores)])
            avg_seconds = sum([test['test_write']['avg_seconds'] for test in results]) / len(results)
            return {'test_write_mp': {
                'chunk_file': chunk_file,
                'cores': cores,
                'iterations': n,
                'avg_seconds': avg_seconds
            }}

    def test_mixed_mp(self, chunk_file: str, cores: int = 4, n: int = 10) -> dict[str, any]:
        with mp.Pool(cores) as pool:
            args = []
            for c_idx in range(cores):
                args.append(('read' if c_idx % 2 else 'write', chunk_file, n))
            results = pool.starmap(self._work, args)

            _r_cnt = _w_cnt = 0
            avg_read_seconds = avg_write_seconds = 0.
            for res in results:
                if read_res := res.get('test_read'):
                    _r_cnt += 1
                    avg_read_seconds += read_res.get('avg_seconds')
                elif write_res := res.get('test_write'):
                    _w_cnt += 1
                    avg_write_seconds += write_res.get('avg_seconds')
            avg_read_seconds /= _r_cnt
            avg_write_seconds /= _w_cnt

            return {'test_mixed_mp': {
                'read_operation': self.READ_QUERY,
                'write_chunk_file': chunk_file,
                'cores': cores,
                'iterations': n,
                'avg_read_seconds': avg_read_seconds,
                'avg_write_seconds': avg_write_seconds
            }}
