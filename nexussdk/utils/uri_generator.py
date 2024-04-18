import uuid
import random as rd
import pandas as pd
rnd = rd.Random()

def generate_uri_column(df: pd.DataFrame, uri_field_name, nexus_uri_base, uri_salt_field_list, uri_salt, uri_salt_delimiter):

    if len(df) > 0:

        # Create a salt column with a fixed value for all rows
        df['_salt'] = uri_salt

        # Combine all fields to be used in URI generation
        combined_fields = df[uri_salt_field_list + ['_salt']].fillna('').astype(str).agg(uri_salt_delimiter.join, axis=1)

        # Vectorized URI generation
        df[uri_field_name] = combined_fields.apply(lambda x: _generate_uri(nexus_uri_base, x))
        
        # Drop the temporary '_salt' column
        df.drop('_salt', axis=1, inplace=True)

    else:
        df[uri_field_name] = None

    return df


def generate_uri(nexus_uri_base, seed_value):
    
    rnd.seed(seed_value)
    random_uuid = uuid.UUID(int=rnd.getrandbits(128), version=4)
    random_uri = f"{nexus_uri_base}{str(random_uuid)}"
    return random_uri
