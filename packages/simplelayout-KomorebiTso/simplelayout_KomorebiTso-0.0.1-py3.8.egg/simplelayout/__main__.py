from simplelayout.cli.cli_generate import get_options
from simplelayout.generator.core import generate_matrix
from simplelayout.generator.utils import save_fig
from simplelayout.generator.utils import save_matrix
from simplelayout.generator.utils import make_dir


def main():
    option = get_options()
    x = generate_matrix(
        option.board_grid, option.unit_grid, option.unit_n, option.positions)
    make_dir(option.outdir)
    file_path = option.outdir + '/' + option.file_name
    save_matrix(x, file_path)
    save_fig(x, file_path)


if __name__ == "__main__":
    main()
