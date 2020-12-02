import collections
import functools
import numpy as np
import operator

IMAGEOutput = collections.namedtuple(
    "IMAGEOutput", ("data", "years", "header", "unit", "label")
)


def load_image_data_file(fp):
    raw = list(open(fp))

    # Remove empty strings at end of file
    if not raw[-1]:
        raw = raw[:-1]

    if len(raw) == 1 or (len(raw) == 2 and "!" in raw[0]):
        return None

    unit = label = ""
    format = "comma-separated"
    if raw[0][0] == "!":
        format = "space-separated"
        for elem in raw[0].split(";"):
            if "Unit=" in elem:
                unit = elem.replace("Unit=", "").strip()
            elif "Label=" in elem:
                unit = elem.replace("Label=", "").strip()
        raw = raw[1:]

    if format == "comma-separated":
        header, years, data = get_comma_separated_data(raw)
    else:
        header, years, data = get_space_separated_data(raw)

    return IMAGEOutput(data, years, header, unit, label)


def get_comma_separated_data(raw):
    # Convert to long string
    header, data = "".join(raw).strip().split(" = ")

    # Remove trailing comma
    assert data[-1] == ";"
    data = data[:-1]

    # Remove newline characters and convert to list
    data = eval(data.replace("\n", ""))

    shape = tuple(eval(header[header.index("[") : header.index("]") + 1]))
    step_size = functools.reduce(operator.mul, shape) + 1
    years = np.array(data[::step_size], dtype=int)

    data = np.stack(
        [
            np.array(data[1 + index * step_size : (index + 1) * step_size]).reshape(
                shape
            )
            for index in range(len(years))
        ],
        axis=-1,
    )

    return header, years, data


def get_space_separated_data(raw):
    assert raw[0].strip().endswith("= [")
    assert raw[-1].strip().endswith("];")

    header = raw[0].replace("= [", "").strip()
    shape = tuple(eval(header[header.index("[") : header.index("]") + 1]))
    data = [eval(line.strip().replace("  ", ",")) for line in raw[1:-1]]

    if len(shape) == 1:
        step_size = 1
    else:
        step_size = functools.reduce(operator.mul, shape[:-1])

    years = np.array(data[:: step_size + 1], dtype=int)

    subarrays = [
        np.array(
            data[index * (step_size + 1) + 1 : (index + 1) * (step_size + 1)]
        ).reshape(shape)
        for index in range(len(years))
    ]
    return header, years, np.stack(subarrays, axis=-1)
