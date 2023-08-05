import math
import multiprocessing


def get_available_cpu_count(cpu_count=-1):
    max_cpu_count = multiprocessing.cpu_count()
    return max_cpu_count if cpu_count == -1 or cpu_count > max_cpu_count else cpu_count


def split_data(data, chunks_count):
    data_size = len(data)
    chunk_size = int(data_size / chunks_count)
    rest = data_size % chunks_count
    left_border = 0
    chunks = []

    for i in range(chunks_count):
        current_chunk_size = chunk_size
        if rest > 0:
            current_chunk_size += 1
            rest -= 1

        chunks.append(data[left_border:left_border + current_chunk_size])
        left_border += current_chunk_size

    return chunks


def roundup(x, step=10):
    return int(math.ceil(x / step)) * step
