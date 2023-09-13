from .project import Project
import sys

try:
    out = sys.argv[2]
except IndexError:
    out = None

if out:
    Project(sys.argv[1], out).generate()
else:
    Project(sys.argv[1]).generate()
