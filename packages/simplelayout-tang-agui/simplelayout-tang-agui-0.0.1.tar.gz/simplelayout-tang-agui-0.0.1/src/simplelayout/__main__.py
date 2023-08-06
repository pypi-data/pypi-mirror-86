from .generator import core
from .generator import utils
from simplelayout.cli import get_options


def main():
    positions_params = get_options()
    generated_matrix = core.generate_matrix(
        positions_params.board_grid, positions_params.unit_grid,
        positions_params.unit_n, positions_params.positions
    )
    utils.make_dir(positions_params.outdir)
    utils.save_matrix(generated_matrix, positions_params.outdir +
                      '/' + positions_params.file_name)
    utils.save_fig(generated_matrix, positions_params.outdir +
                   '/' + positions_params.file_name)


if __name__ == "__main__":
    main()
