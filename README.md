# Unit converter
For the GCI task from CCExtractor.

## Usage
Requires a `conversions.txt` file in the same directory.

Run the Python 3 program. It will prompt the user for details about the conversion they are making. **Make sure that the units used are exactly identical to the ones defined in the `conversions.txt` file.** For example `1 meter/second` won't work as input if your defined units are *meters* or *seconds*, for example.

## Features
The provided `conversions.txt` file has some good examples of the features that are available.

- For example, you can see that `feet-inches: 12` is defined as the conversion from feet to inches. From this, the program can also automatically calculate the conversion from inches to feet.

- Furthermore, the program is able to **find conversions** where they are not explicitly defined. For example, using the provided `conversions.txt`, converting inches to yards goes through 3 conversions:
```
Enter conversion in format "{NUMBER} {INPUT_UNIT} to {OUTPUT_UNIT}" (e.g. 2 meters to feet): 1 inches to yards
Converting 1.0 inches --> centimeters --> meters --> yards... 1.0 inches = 0.02777767900005334 yards

Answer: 0.02777767900005334 yards
```

- The program can do conversions with more **complex units**, without defining them explicitly. For example, if `kilometers-meters: 1000` and `hours-minutes: 60` are provided, it can convert from kilometers/hours to meters/minutes automatically. This is not hard-coded, meaning that it can also convert seconds/kilometers to hours/meters, if needed.

- It is also smart enough to do a conversion when it is possible, even if the units *aren't* defined in the `conversions.txt` file. For example, it can convert from metres/decade to kilometres/decade, without knowing what a decade is in the first place. As long as the numerator or denominator on both sides is the same, it can still convert.

- It can also do **flipped conversions**. For example it can convert from seconds/joules to joules/seconds, or from meters/seconds to hours/kilometers.

- There is a system of **replacements**. For example, some countries use "meters" while others use "metres". In the `conversions.txt` file, you can write a replacement: if the rest of the conversions use "meters" but you want to also support "metres" without writing out all the conversions again, simply write `metres = meters` (notice that this uses equals instead of colon). The program will figure it out.

- **Replacements work for complex units** too! For example, you can write `watts = joules/seconds`. Then you can ask the program to convert from watts to joules/seconds, or kilojoules/hours to watts, or even days/kilocalories to kilowatts (with the configuration in the provided `conversions.txt`).

## Complex examples
These are a list of example conversions that the program can do:
- `5 metres/seconds to seconds/metres` outputs 0.2 seconds/metre. Notice that the program replies with the units that the user provides ("metres") even though it uses "meters" for all the conversions.
- `45 kilometres/hours to minutes/miles` outputs 2.145791931334658 minutes/miles. This is a complex flipped conversion.
- `0.4 days/kilocalories to watts` outputs 0.12106481481481479 watts. This is a complex flipped conversion with a replacement! *Even Google can't do this kind of conversion!*
