import os
import subprocess

def run_script(script_name):
    """
    Run a Python script using subprocess.

    Args:
        script_name (str): The name of the script to run.
    """
    try:
        script_path = os.path.expanduser(f"~/gikoru/py/{script_name}")
        if os.path.exists(script_path):
            print(f"Running {script_name}...")
            subprocess.run(["python3", script_path], check=True)
            print(f"{script_name} completed successfully.")
        else:
            print(f"Error: {script_name} does not exist.")
    except Exception as e:
        print(f"An error occurred while running {script_name}: {e}")

def run_all_scripts():
    """
    Run all scripts in the specified order.
    """
    scripts = [
        "assure_public_reset.py",
        "move_static.py",
        "generate_sections.py",
        "generate_sections_list.py",
        "generate_sections_index.py",
        "generate_sectionsportal.py",
        "generate_sectionsportal_index.py",
        "generate_home_list.py",
        "generate_home_index.py",
        "read_drafts.py",
        "content_maker.py",
        "content_merger.py",
        "generate_otherpages.py",
        "atomizer.py"

    ]
    
    for script in scripts:
        run_script(script)
        
    # ♡♡♡♡♡♡♡♡♡
    print("\n\n♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡\n\n")
    print("ALL HAIL THE ARCH DUKE!")
    print("PLAY GIKOPOI FOR FREE TODAY")
    print("「 https://play.gikopoi.com 」\n")
    print("ギコル~~~~~~~~~~！！！！！！！！！")
    print("done.  (´｡• ᵕ •｡`) ♡\n\n")
    print("♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡♡\n\n")



if __name__ == "__main__":
    run_all_scripts()
