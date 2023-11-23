import glob
import os
import subprocess
import utils.settings as settings

def osm2obj():
    # Define the path to your bash script
    bash_script = settings.OSM2WORLD_DIR+'osm2world.sh'

    # Construct the pattern
    pattern = os.path.join(settings.ASSETS_DIR, '*.osm')

    # Get list of files matching the pattern
    matching_files = glob.glob(pattern)
    print(matching_files)
    cwd = os.getcwd()+"/"

    for input_variable in matching_files:
        input_variable = cwd+input_variable
        output_variable = cwd+settings.OBJ_DIR+input_variable.split(settings.ASSETS_DIR)[-1].split(".osm")[0]+".obj"
        try:
            print(f'{bash_script} -i {input_variable} -o {output_variable}')
            result = subprocess.run([bash_script, '-i', input_variable, '-o', output_variable], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Script returned an error: {e}")