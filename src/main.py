import sys
from converter import generate_pages_recursive
from update import refresh_environment

def main():

    source_dir = "/home/kenjc/development/projects/static_site_generator/static_site/content"
    dest_dir = "/home/kenjc/development/projects/static_site_generator/static_site/static"
    template_path = "/home/kenjc/development/projects/static_site_generator/static_site/template.html"

    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    print(f"Starting build with basepath: {basepath}")
    generate_pages_recursive(source_dir, template_path, dest_dir, basepath=basepath)
    refresh_environment()



if __name__ == "__main__":
    main()
