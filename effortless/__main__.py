from .project import Project
import sys

try:
    Project(sys.argv[1], sys.argv[2]).generate()
except IndexError:
    try:
        Project(sys.argv[1]).generate()
    except IndexError:
        print("Usage: python -m effortless <project_config> [output_dir]")
