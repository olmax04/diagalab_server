def format_float(string_value:str):
    try:
        temp_string = string_value.replace(" PLN", "").replace(",", ".").replace(" ", "")
        f = float(temp_string)
        return f
    except ValueError:
        print(f"Cannot convert {string_value} to a float.")
