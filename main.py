import subprocess

# List of Python scripts to run
scripts = ["1_step.py", "2_step.py", "3_step.py" ,"1_step.py", "2_step1.py", "3_step.py"  , "1_step.py", "2_step2.py", "3_step.py,", "1_step.py", "2_step3.py", "3_step.py", "1_step.py", "2_step4.py", "3_step.py", "1_step.py", "2_step5.py", "3_step.py"]

while True:
    for script in scripts:
        try:
            print(f"Running {script}...")
        
            # Run the script in a separate process
            result = subprocess.run(
                ["python", script], 
                capture_output=True,  # Capture stdout and stderr
                text=True             # Decode output as text
                )
        
                # Check the result
            if result.returncode == 0:
                print(f"Output of {script}:\n{result.stdout}")
            else:
                print(f"Error in {script}:\n{result.stderr}")
    
        except Exception as e:
            print(f"An error occurred while running {script}: {e}")
    
        print(f"Finished {script}.\n{'-' * 50}")
