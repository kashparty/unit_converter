def convert(input_value, input_unit, output_unit, conversion_table):
    if input_unit == output_unit:
        return (True, input_value)

    # First find conversion path
    units_visited = [input_unit]
    current_units = [input_unit]
    new_units = []
    paths = {}

    while len(current_units) > 0:
        for unit in current_units:
            for key in conversion_table.keys():
                if unit == key[0] and key[1] not in units_visited:
                    new_units.append(key[1])
                    units_visited.append(key[1])
                    paths[unit] = new_units


            if output_unit in units_visited:
                # Conversion is possible

                final_path = [output_unit]
                to_unit = output_unit
                while to_unit not in paths[input_unit]:
                    for key in paths.keys():
                        if to_unit in paths[key]:
                            final_path.insert(0, key)
                            to_unit = key

                output = f"Converting {input_value} {input_unit}"
                current_value = input_value
                current_unit = input_unit
                for next_unit in final_path:
                    output += f" --> {next_unit}"
                    current_value *= conversion_table[(current_unit, next_unit)]
                    current_unit = next_unit

                print(
                    output + f"... {input_value} {input_unit} = {current_value} {output_unit}")
                return (True, current_value)

        current_units = new_units
        new_units = []

    return (False, None)


conversion_table = {}
replacements = {}

with open("conversions.txt", "r") as f:
    lines = f.read().splitlines()
    for line in lines:
        if ":" in line:
            conversion = line.split(":")
            units = conversion[0].strip()
            value = conversion[1].strip()

            conversion_table[tuple(units.split("-"))] = float(value)
            # If supplied with metres-feet, store feet-metres too
            conversion_table[tuple(units.split("-")[::-1])] = 1 / float(value)
        elif "=" in line:
            replacement = line.split("=")
            replacements[replacement[0].strip()] = replacement[1].strip()

all_units = list(zip(*conversion_table.keys()))[0] # Lists at indexes 0 and 1 are identical

[input_value, original_input_unit, _, original_output_unit] = input(
    "Enter conversion in format \"{NUMBER} {INPUT_UNIT} to {OUTPUT_UNIT}\" (e.g. 2 meters to feet): ").split(" ")

if original_input_unit in replacements.keys():
    input_unit = replacements[original_input_unit]
else:
    input_unit = original_input_unit

if original_output_unit in replacements.keys():
    output_unit = replacements[original_output_unit]
else:
    output_unit = original_output_unit

try:
    input_value = float(input_value)
except ValueError:
    print("Input value must be a number")
else:
    if "/" in input_unit and "/" in output_unit:
        # Complex conversion!
        [upper_input_unit, lower_input_unit] = input_unit.split("/")
        [upper_output_unit, lower_output_unit] = output_unit.split("/")
        upper_input_value = input_value
        lower_input_value = 1

        # If a unit isn't defined in the conversions table and it's different for input and output quit.
        # However, if a unit isn't defined but it's the same for input and output, continue.
        if upper_input_unit not in all_units:
            if upper_input_unit != upper_output_unit:
                print(f"{upper_input_unit} is an unkwown unit. Use the exact name specified in the conversions file.")
                quit()
        elif upper_output_unit not in all_units:
            print(f"{upper_output_unit} is an unkwown unit. Use the exact name specified in the conversions file.")
            quit()
        if lower_input_unit not in all_units:
            if lower_input_unit != lower_output_unit:
                print(f"{lower_input_unit} is an unkwown unit.Use the exact name specified in the conversions file.")
                quit()
        elif lower_output_unit not in all_units:
            print(f"{lower_output_unit} is an unkwown unit. Use the exact name specified in the conversions file.")
            quit()

        upper_output_value = convert(upper_input_value, upper_input_unit, upper_output_unit, conversion_table)
        lower_output_value = convert(lower_input_value, lower_input_unit, lower_output_unit, conversion_table)

        if upper_output_value[0] and lower_output_value[0]:
            print(f"\nAnswer: {upper_output_value[1] / lower_output_value[1]} {original_output_unit}")
        else:
            print("Error: Conversion not possible.")
    else:
        answer = convert(input_value, input_unit, output_unit, conversion_table)

        # If a unit isn't defined in the conversions table and it's different for input and output quit.
        # However, if a unit isn't defined but it's the same for input and output, continue.
        if input_unit not in all_units and input_unit != output_unit:
            print(f"{input_unit} is an unkwown unit. Use the exact name specified in the conversions file.")
            quit()
        if output_unit not in all_units:
            print(f"{output_unit} is an unkwown unit. Use the exact name specified in the conversions file.")

        if answer[0]:
            print(f"\nAnswer: {answer[1]} {original_output_unit}")
        else:
            print("Error: Conversion not possible.")
