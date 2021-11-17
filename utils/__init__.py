def columns_to_dict(df, col1, col2):
    return dict(zip(df[col1], df[col2]))


def get_all_countries(df, name, code=None, return_as_df=True):
    """[summary]

    Args:
        df ([type]): [description]
        name ([type]): [description]
        code ([type]): [description]
    """
    countries = (
        df[[name, code]].drop_duplicates()
        if code is not None
        else df[[name]].drop_duplicates()
    )
    assert (
        len(countries) == df[name].nunique()
    ), "The unique number of countries does not equal to the unique number of country-code combinations"

    print(f"Number of distinct countries in this dataset: {len(countries)}")
    if return_as_df:
        return countries
    else:
        if code is None:
            lst = countries[0].tolist()
            print("No country code for this dataset. Only return a list")
            print(f"Number of distinct countries in this dataset: {len(lst)}")
            return lst
        else:
            dic = columns_to_dict(countries, name, code)
            return dic
