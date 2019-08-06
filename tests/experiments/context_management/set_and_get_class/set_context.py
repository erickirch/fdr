import tests.experiments.context_management.set_and_get_class.context_manager as cm
import tests.experiments.context_management.set_and_get_class.funcs as f

with cm.worksheet_columns.set('worksheet columns'):#, cm.fields.set('fields'):
    f.print_ws_cols()
    f.print_fields()
