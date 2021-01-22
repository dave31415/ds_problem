from validate import validate_file


def main(*args):
    use_corrupt = True
    filename = args[0]
    if len(args) > 1:
        if args[1] == 'score':
            use_corrupt = False

    validate_file(filename, use_corrupted=use_corrupt)
