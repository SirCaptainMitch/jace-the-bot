from rich.console import Console

console = Console()


def get_params():
    return dict(
        name='Mitch'
        , random_tidbit='column_names_should_be_plural'
    )


console.print(
    parameters := get_params()
)

parameters['random_tidbit'] = 'column_names_should_be_singular'
console.print(parameters)


