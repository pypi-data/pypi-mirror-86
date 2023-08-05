import os
import sys
from typing import NoReturn

from traceback_with_variables.color import choose_color_scheme
from traceback_with_variables.core import iter_tb_lines, ColorScheme, ColorSchemes


def override_print_tb(
    max_value_str_len: int = 1000,
    max_exc_str_len: int = 10000,
    ellipsis_: str = '...',
    num_context_lines: int = 1,
    activate_by_env_var: str = '',
    deactivate_by_env_var: str = '',
    color_scheme: ColorScheme = ColorSchemes.auto,
) -> NoReturn:
    if (activate_by_env_var and not os.getenv(activate_by_env_var, '')) or \
            (deactivate_by_env_var and os.getenv(deactivate_by_env_var, '')):
        return

    def excepthook(
        e_cls,  # noqa
        e,
        tb
    ):
        for line in iter_tb_lines(
            e=e,
            tb=tb,
            num_context_lines=num_context_lines,
            max_value_str_len=max_value_str_len,
            max_exc_str_len=max_exc_str_len,
            ellipsis_=ellipsis_,
            color_scheme=choose_color_scheme(color_scheme, sys.stderr),
        ):
            sys.stderr.write(line)
            sys.stderr.write('\n')

        sys.stderr.flush()

    sys.excepthook = excepthook
