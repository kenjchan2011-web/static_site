from converter import generate_pages_recursive
from update import refresh_environment

def main():

    source_dir = "/home/kenjc/development/projects/static_site_generator/static_site/content"
    dest_dir = "/home/kenjc/development/projects/static_site_generator/static_site/static"
    template_path = "/home/kenjc/development/projects/static_site_generator/static_site/template.html"

    generate_pages_recursive(source_dir, template_path, dest_dir)
    refresh_environment()



if __name__ == "__main__":
    main()
