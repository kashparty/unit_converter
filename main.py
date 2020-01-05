def find_penultimate_conversion(input_unit, output_unit, conversion_table):
    units_to_explore = [input_unit]
    units_explored = []

    while output_unit not in units_explored:
        while len(units_to_explore) > 0:
            unit_to_explore = units_to_explore[0]

            units_explored.append(unit_to_explore)
            units_to_explore.pop(0)
            for conversion in conversion_table.keys():
                if conversion[0] == unit_to_explore and conversion[1] not in units_explored:
                    if output_unit == conversion[1]:
                        return (True, conversion[0])
                    else:
                        units_to_explore.append(conversion[1])

            if len(units_to_explore) == 0:
                return (False, None)

def convert(value, input_unit, output_unit, conversion_table):
    if input_unit == output_unit:
        return (True, value)

    target_unit = output_unit
    path = []
    while target_unit != input_unit:
        path.insert(0, target_unit)
        result = find_penultimate_conversion(input_unit, target_unit, conversion_table)
        target_unit = result[1]
        if result[0] == False:
            return (False, None)

    print(f"\n{value} {input_unit}")

    current_unit = input_unit
    for next_unit in path:
        value *= conversion_table[(current_unit, next_unit)]
        print(f" = {value} {next_unit}")
        current_unit = next_unit

    return (True, value)


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

# Replacements e.g. watts -> joules/seconds
input_unit = replacements.setdefault(original_input_unit, original_input_unit)
output_unit = replacements.setdefault(original_output_unit, original_output_unit)

try:
    input_value = float(input_value)
except ValueError:
    print("Input value must be a number")
else:
    if "/" in input_unit and "/" in output_unit:
        # Complex conversion!
        [upper_input_unit, lower_input_unit] = input_unit.split("/")
        [upper_output_unit, lower_output_unit] = output_unit.split("/")

        # Replacements e.g. kilometres -> kilometers
        upper_input_unit = replacements.setdefault(upper_input_unit, upper_input_unit)
        lower_input_unit = replacements.setdefault(lower_input_unit, lower_input_unit)
        upper_output_unit = replacements.setdefault(upper_output_unit, upper_output_unit)
        lower_output_unit = replacements.setdefault(lower_output_unit, lower_output_unit)

        upper_input_value = input_value
        lower_input_value = 1

        # If a unit isn't defined in the conversions table and it's different for input and output, quit.
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
                print(f"{lower_input_unit} is an unkwown unit. Use the exact name specified in the conversions file.")
                quit()
        elif lower_output_unit not in all_units:
            print(f"{lower_output_unit} is an unkwown unit. Use the exact name specified in the conversions file.")
            quit()

        upper_output_value = convert(upper_input_value, upper_input_unit, upper_output_unit, conversion_table)
        lower_output_value = convert(lower_input_value, lower_input_unit, lower_output_unit, conversion_table)

        # If conversion was successful, print answer. Otherwise, try flipped conversion.
        if upper_output_value[0] and lower_output_value[0]:
            print(f"\nAnswer: {upper_output_value[1] / lower_output_value[1]} {original_output_unit}")
        else:
            # Try swapping the numerator and denominator for flipped conversion
            temp = upper_output_unit
            upper_output_unit = lower_output_unit
            lower_output_unit = temp

            upper_output_value = convert(
                upper_input_value, upper_input_unit, upper_output_unit, conversion_table)
            lower_output_value = convert(
                lower_input_value, lower_input_unit, lower_output_unit, conversion_table)

            # If conversion was successful, print answer
            if upper_output_value[0] and lower_output_value[0]:
                print(
                    f"\nAnswer: {lower_output_value[1] / upper_output_value[1]} {original_output_unit}")
            else:
                print("Error: Conversion not possible.")

    else:
        # Simple conversion

        # If a unit isn't defined in the conversions table and it's different for input and output quit.
        # However, if a unit isn't defined but it's the same for input and output, continue.
        if input_unit not in all_units and input_unit != output_unit:
            print(f"{input_unit} is an unkwown unit. Use the exact name specified in the conversions file.")
            quit()
        if output_unit not in all_units:
            print(f"{output_unit} is an unkwown unit. Use the exact name specified in the conversions file.")
            quit()

        answer = convert(input_value, input_unit, output_unit, conversion_table)

        # If conversion was successful, print answer
        if answer[0]:
            print(f"\nAnswer: {answer[1]} {original_output_unit}")
        else:
            print("Error: Conversion not possible.")
