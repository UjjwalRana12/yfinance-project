
def export_to_excel(df, file_name):
    df.index = df.index.tz_localize(None)
    df.to_excel(file_name)
    print(f"Data has been exported to {file_name}")
