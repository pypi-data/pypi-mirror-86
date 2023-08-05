import sys
import click
import pandas as pd
import pathlib

PATH_TO_OUTPUT = "output/"
FILE_NAME = "out.csv"


@click.group()
@click.version_option("1.0.0")
def main():
    """
    Simple command-line application to manage the last watched series
    """
    pass


# Add new title to the list
@main.command()
@click.argument("name")
def add(name):
    """
    Add new title to the list.\n
    Arguments:\n
        NAME - name of the title.
    """
    # Create series
    s = create_correct_s(name)
    # Load the dataframe
    loaded_df = load_df()

    # Check is dataframe loaded successfully
    if isinstance(loaded_df, int):
        df = pd.DataFrame(s).T
    else:
        df = add_s_to_df(s, loaded_df)

    # Save the result data frame
    save_df(df)
    click.echo("Successfully added.")
    click.echo(df)


# Remove title from the list by id
@main.command()
@click.argument("title_id")
def remove(title_id):
    """
    Remove title from list by title's id or name.\n
    Arguments:\n
        TITLE_ID  name or id of title
    """

    # Load the dataframe
    loaded_df = load_df()
    # Check is dataframe loaded successfully
    if isinstance(loaded_df, int) or loaded_df.empty:
        click.echo("There are currently no any titles.")
    else:
        # Check if this title is in the list
        b = False
        if title_id in loaded_df.values:
            b = True
        elif isinstance(title_id, int):
            if int(title_id) in loaded_df.index:
                b = True
        if b:
            # Remove this title
            if title_id.isdigit():
                id = int(title_id)
                loaded_df.drop(id, inplace=True)
            else:
                index_names = loaded_df[loaded_df['Name'] == title_id].index
                loaded_df.drop(index_names, inplace=True)

            # Save new dataframe
            save_df(loaded_df)

            # Print results
            click.echo("Successfully removed")
            if not loaded_df.empty:
                click.echo(loaded_df)

        else:
            # Print error
            click.echo("Can't find title with id = " + title_id)


# Print all titles, paths and series
@main.command()
def show():
    """
    Show all titles.
    """
    # Load the dataframe
    loaded_df = load_df()
    # Check is dataframe loaded successfully
    if isinstance(loaded_df, int) or loaded_df.empty:
        click.echo("There are currently no any titles.")
    else:
        click.echo(loaded_df.get(["Name", "Series"]).to_string())


@main.command()
@click.argument("title_id")
@click.argument("series", type=click.INT)
def set(title_id, series):
    """
    Set certain series to the title.\n
    Arguments:\n
        TITLE_ID  Name or id of title.\n
        SERIES    New value.
    """
    # Load dataframe with all titles
    loaded_df = load_df()

    if isinstance(loaded_df, int) or loaded_df.empty:
        click.echo("There are currently no titles.")
    else:
        if title_id.isdigit():
            loaded_df.at[int(title_id), "Series"] = series
        else:
            loaded_series = loaded_df[loaded_df['Name'] == title_id]
            loaded_df.at[loaded_series.index, "Series"] = series
        click.echo(loaded_df)
        save_df(loaded_df)


# Create new series with name, path, and series columns
def create_correct_s(name):
    return pd.Series([name, 0], index=["Name", "Series"])


# Add series to the existing dataframe
def add_s_to_df(s, df):
    df = pd.concat([df, s.to_frame().T], ignore_index=True)
    return df


# Load csv from PATH_TO_OUTPUT
# Return 0 if file not found
def load_df():
    try:
        return pd.read_csv(PATH_TO_OUTPUT + FILE_NAME,  index_col=0)
    except FileNotFoundError:
        return 0


# Save df dataframe to PATH_TO_OUTPUT path
def save_df(df):
    try:
        df.to_csv(PATH_TO_OUTPUT + FILE_NAME)
    except FileNotFoundError:
        pathlib.Path(PATH_TO_OUTPUT).mkdir(parents=True, exist_ok=True)
        df.to_csv(PATH_TO_OUTPUT + FILE_NAME)
    return 0


# Main method
if __name__ == '__main__':
    args = sys.argv
    main()
