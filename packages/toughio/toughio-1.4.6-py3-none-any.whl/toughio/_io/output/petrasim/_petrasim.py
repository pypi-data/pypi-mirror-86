from __future__ import with_statement

import numpy

from .._common import to_output

__all__ = [
    "read",
    "write",
]


def read(filename, file_type, file_format, labels_order):
    """Read Petrasim OUTPUT_ELEME.csv."""
    with open(filename, "r") as f:
        # Headers
        line = f.readline().strip()
        headers = [header.strip() for header in line.split(",")[3:]]

        # Data
        times, elements, data = [], [], []
        while True:
            line = f.readline().strip()

            if line:
                line = line.split(",")
                times.append(float(line[0]))
                elements.append(line[1].strip())
                data.append([float(x) for x in line[3:]])
            else:
                break

    times = numpy.array(times)
    elements = numpy.array(elements)
    data = numpy.array(data)

    labels, unique_times, variables = [], [], []
    for time in numpy.unique(times):
        idx = times == time
        labels.append(elements[idx])
        unique_times.append(time)
        variables.append(data[idx])

    return to_output(
        file_type, file_format, labels_order, headers, unique_times, labels, variables
    )


def write(filename, output):
    """Write Petrasim OUTPUT_ELEME.csv."""
    out = output[-1]
    headers = []
    headers += ["X"] if "X" in out.data.keys() else []
    headers += ["Y"] if "Y" in out.data.keys() else []
    headers += ["Z"] if "Z" in out.data.keys() else []
    headers += [k for k in out.data.keys() if k not in {"X", "Y", "Z"}]

    with open(filename, "w") as f:
        # Headers
        record = ",".join(
            "{:>18}".format(header)
            for header in ["TIME [sec]", "ELEM", "INDEX"] + headers
        )
        f.write("{}\n".format(record))

        # Data
        for out in output:
            data = numpy.transpose([out.data[k] for k in headers])
            formats = ["{:20.12e}", "{:>18}", "{:20d}"]
            formats += ["{:20.12e}"] * len(out.data)

            i = 0
            for d in data:
                tmp = [out.time, out.labels[i], i + 1]
                tmp += [x for x in d]
                record = ",".join(fmt.format(x) for fmt, x in zip(formats, tmp))
                f.write("{}\n".format(record))
                i += 1
