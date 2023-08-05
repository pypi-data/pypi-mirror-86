# checkpointe
A simple progress timer/memory tracker for debugging python scripts.

## Overview
Checkpointe is a tool for locating areas of code that are time or memory-intensive. This allows the user to:
* Track specific function calls in real-time
* Tag specific checkpoints with an identifying message
* Analyze a final output that shows time and percentage of time between each checkpoint
* Reorder checkpoints easily without having to refactor code
* Analyze memory usage to determine where usage is peaking

## Requires
* datetime
* tracemalloc (for memory tracking)

## Installation
Checkpointe is available for download using pip:

    pip install checkpointe

## Using Checkpointe

### Start
To start tracking time and/or memory, initialize checkpointe with the .start() function

    import checkpointe as check

    check.start(summary=True, verbose=True, memory=True)

Setting these defaults determines the level of detail checkpointe prints to stdout:
* summary (default = True): prints a summary after calling the `.stop()` method
* verbose (default = False): if enabled, outputs data at each check point
* memory (default = False): if enabled, tracks and outputs information about system memory usage

### Point
Call the `.point()` method to create a marker at any point in the code.

    add = 2 + 2
    
    check.point("ADDITION")

    mult = 2 * 2

    check.point("MULTIPLICATION")

    exp = 2 ** 2

    check.point("EXPONENTIAL")

If `verbose=True`, a statement will be printed at each checkpoint.

### Stop
When you are ready to stop tracking, call the `.stop()` method.

    check.stop()

If `summary=True`, a summary statement will be printed. Each marker will be displayed, along with the time elapsed since the previous marker and the percentage of overall time elapsed.

If `memory=True`, a final memory statement will be printed, with memory usage at each marker, along with the peak memory usage noted at each marker.

## Future Development
Future versions will enable integration with logging to an output file.
