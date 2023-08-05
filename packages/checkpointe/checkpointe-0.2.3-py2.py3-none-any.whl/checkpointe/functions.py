import datetime as dt
import tracemalloc

def start(summary=True, verbose=False, memory=False):
	
	# Set global variables
	global checkpoints_global
	global report_global
	global realtime_global
	global memory_global
	checkpoints_global = []
	report_global = summary
	realtime_global = verbose
	memory_global = memory
	
	# Set marker
	time = dt.datetime.now()
	marker = "Process Start"
	entry = (time, marker)
	checkpoints_global.append(entry)

	# Tracking memory if enabled
	if memory_global:
		tracemalloc.start()
	else:
		pass
	
	# Print marker
	if realtime_global:
	    print(marker)
	else:
		pass


def point(marker=None):
	
	# Set marker
	time = dt.datetime.now()

	# Capture memory usage
	if memory_global:

		current, peak = tracemalloc.get_traced_memory()

		if marker:
			entry = (time, marker, current, peak)
		else:
			entry = (time, None, current, peak)

	else:

		if marker:
			entry = (time, marker, None, None)
		else:
			entry = (time, None, None, None)		
		checkpoints_global.append(entry)
	
	# Print marker
	if realtime_global:
	    # Calculate elapsed time
	    marker_start = checkpoints_global[0][0]
	    marker0 = checkpoints_global[-2][0]
	    marker1 = checkpoints_global[-1][0]
	    elapsed = marker1 - marker_start
	    marker_time = marker1 - marker0
	    
	    # Compile update
	    point_number = len(checkpoints_global) - 1
	    if marker:
	    	update = f"Step {point_number}: {marker} \n Time: {marker_time} / {elapsed}"
	    else:
	    	update = f"Step {point_number}: {marker_time} / {elapsed}"

		# Adding memory update if requested
		if current:
			update += f"\n Current memory usage: {current / 10**6}MB / Peak: {peak / 10**6}MB"
		else:
			pass
	    
	    print(update)
	else:
		pass
		
def stop():
	
	print("")
	print("###########################")
	print("Checkpoint Summary")
	
	# Set marker
	time = dt.datetime.now()
	marker = "Process Complete"
	entry = (time, marker)		
	checkpoints_global.append(entry)
	
	# Set variables
	start = checkpoints_global[0][0]
	end = checkpoints_global[-1][0]
	elapsed = end - start
	
	if report_global:
		for n in range(1,len(checkpoints_global)):
			point0 = checkpoints_global[n-1][0]
			point1 = checkpoints_global[n][0]
			time = point1 - point0
			mark = checkpoints_global[n][1]
			pct = round((time / elapsed) * 100, 1)
			
			if mark:
				step = f"{n}: {mark} | {time} / {elapsed} | {pct}%"
			else:
				step = f"{n}: {time} / {elapsed}"
				
			print(step)

		if memory_global:
			tracemalloc.stop()
			print('\n##########################################\n')
			for n in range (1, len(checkpoints_global)):
				current = checkpoints_global[n][2]
				peak = checkpoints_global[n][3]

			if mark:
				step = f"{n}: {mark} | Current: {current / 10**6}MB / Peak: {peak / 10**6}MB"
			else:
				step = f"{n}: Current: {current / 10**6}MB / Peak: {peak / 10**6}MB"

			print(step)
			
	else:
		pass

	print("PROCESS COMPLETE")			
	print(f"TOTAL RUN TIME: {elapsed}")