import argparse
import sys


def get_options():
    parser = argparse.ArgumentParser()
    # TODO: 按 1-simplelayout-CLI 要求添加相应参数
    parser.add_argument('--board_grid', type=int, help='square size')
    parser.add_argument('--unit_grid', type=int, help='component size')
    parser.add_argument('--unit_n', type=int, help='component num')
    parser.add_argument('--positions', type=int,
                        nargs='*', help='location index')
    parser.add_argument('-o', '--outdir', type=str,
                        help='save path', default='example_dir')
    parser.add_argument('--file_name', type=str, default='example')

    options = parser.parse_args()

    if options.board_grid % options.unit_grid != 0:
        print('modify unit_grid')
        sys.exit(1)
    if len(options.positions) != options.unit_n:
        print('modify positions list')
        sys.exit(1)
    for i in options.positions:
        if i > (options.board_grid/options.unit_grid)**2 or i < 1:
            print('modify positions num')
            sys.exit(1)

    # if not Path(options.outdir).exists():
    #     Path(options.outdir).mkdir(parents=True, exist_ok=True)

    # file1 = options.outdir + '/' + options.file_name + '.mat'
    # file2 = options.outdir + '/' + options.file_name + '.jpg'
    # fo1 = open(file1, 'w')
    # fo2 = open(file2, 'w')
    # # fo1.write('test/n')
    # # fo2.write('test')
    # fo1.close()
    # fo2.close()

    return options
