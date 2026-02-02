from ast import pattern
import os, sys
import logging
import shutil
from zipfile import Path
from converter import generate_page

TARGET_DIR="./public"
SOURCE_DIR="./static"

# 1. Setup Logging Configuration
logging.basicConfig(
    filename='file_activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a' # 'w' overwrites each time; use 'a' to append
)

def check_public_directory(DIR):

    if not os.path.exists(DIR):
        print(f"Error: The path {DIR} does not exist.")
        return False

    logging.info(f"Starting scan of: {DIR}")
    
    for root, dirs, files in os.walk(DIR):
        # Log the current directory being scanned
        logging.info(f"Directory: {root}")
        
        # Log each file found in that directory
        for name in files:
            logging.info(f"  File: {os.path.join(root, name)}" )

    logging.info("Scan completed successfully.")

    return True    

def delete_public_directory():

    is_public_dir = check_public_directory(TARGET_DIR)

    if is_public_dir == True:
        try:
            # Perform the deletion
            shutil.rmtree(TARGET_DIR)
            
            logging.info(f"SUCCESSFULLY DELETED: {TARGET_DIR} and all its children.")
            print(f"Successfully deleted {TARGET_DIR}")
            
        except Exception as e:
            logging.error(f"FAILED TO DELETE {TARGET_DIR}: {str(e)}")
            print(f"An error occurred: {e}")

def copy_files_to_public_directory():

    is_source_dir = check_public_directory(SOURCE_DIR)

    if is_source_dir:
        try:
            if not os.path.exists(SOURCE_DIR):
                logging.error(f"Source directory '{SOURCE_DIR}' does not exist.")
                return

            # dirs_exist_ok=True allows copying even if 'public' already exists
            # If 'public' doesn't exist, copytree creates it automatically.
            shutil.copytree(SOURCE_DIR, TARGET_DIR, dirs_exist_ok=True)
            
            logging.info(f"Successfully copied {SOURCE_DIR} to {TARGET_DIR}")
            print(f"Deployment complete: {SOURCE_DIR} -> {TARGET_DIR}")

        except Exception as e:
            logging.error(f"Error during copy: {str(e)}")
            print(f"Failed to copy: {e}")

def refresh_environment():
    delete_public_directory()
    copy_files_to_public_directory()

def build_page():

    source_dir = "/home/kenjc/development/projects/static_site_generator/static_site/content"
    dest_dir = "/home/kenjc/development/projects/static_site_generator/static_site/static"
    template_path = "/home/kenjc/development/projects/static_site_generator/static_site/template.html"

    for root, dirs, files in os.walk(source_dir):
        if "index.md" in files:
            full_path = os.path.join(root, "index.md")
            dest_path = full_path.replace(source_dir, dest_dir).replace("index.md", "index.html")
            generate_page(full_path, template_path, dest_path)
            logging.info(f"Generated page: {dest_path}")


#if __name__=="__main__":
    #print(build_page(source_dir, dest_dir))