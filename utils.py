# # import pandas as pd
# # import os

# # def load_all_apartment_data():
# #     folder = "data"
# #     files = [f"apartments_rent_pl_2024_{str(i).zfill(2)}.csv" for i in range(1, 7)]
# #     paths = [os.path.join(folder, f) for f in files]
# #     return pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)


# import pandas as pd
# import os

# def load_all_apartment_data():
#     folder = "data"
#     files = [f"apartments_rent_india_2024_{str(i).zfill(2)}.csv" for i in range(1, 7)]
#     paths = [os.path.join(folder, f) for f in files]
#     return pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)


import pandas as pd
import os

def load_all_apartment_data():
    folder = "data"
    files = [f"apartments_rent_pl_2024_{str(i).zfill(2)}.csv" for i in range(1, 7)]
    paths = [os.path.join(folder, f) for f in files]

    df = pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)

    # Add latitude/longitude if missing
    if 'latitude' not in df.columns:
        df['latitude'] = df['city'].map({
            "Mumbai": 19.0760,
            "Hyderabad": 17.3850,
            "Bengaluru": 12.9716,
            "Delhi": 28.6139,
            "Ahmedabad": 23.0225,
            "Chennai": 13.0827
        }).fillna(20.0)  # fallback latitude

    if 'longitude' not in df.columns:
        df['longitude'] = df['city'].map({
            "Mumbai": 72.8777,
            "Hyderabad": 78.4867,
            "Bengaluru": 77.5946,
            "Delhi": 77.2090,
            "Ahmedabad": 72.5714,
            "Chennai": 80.2707
        }).fillna(78.0)  # fallback longitude

    return df
