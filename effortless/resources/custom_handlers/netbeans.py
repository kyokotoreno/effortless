"""
CustomHandler for NetBeans Project

params: None

"""

from effortless.file import File

class CustomHandler:
    files = [
        {
            'folder': '',
            'origin': '$netbeans',
            'is_bytes': False,
            'name': 'build.xml'
        },
        {
            'folder': '',
            'create': True,
            'name': 'manifest.mf',
            'content': 'Manifest-Version: 1.0\nX-COMMENT: Main-Class will be added automatically by build'
        },
        {
            'folder': 'nbproject',
            'origin': '$netbeans/nbproject',
            'is_bytes': False,
            'name': 'build-impl.xml'
        },
        {
            'folder': 'nbproject',
            'origin': '$netbeans/nbproject',
            'name': 'genfiles.properties'
        },
        {
            'folder': 'nbproject',
            'origin': '$netbeans/nbproject',
            'is_bytes': False,
            'name': 'project.properties'
        },
        {
            'folder': 'nbproject',
            'origin': '$netbeans/nbproject',
            'is_bytes': False,
            'name': 'project.xml'
        },
    ]

    def __init__(self, custom):
        return

    def fromToHandle(to_handle):
        objs = []
        
        if not to_handle == None:
                objs = [CustomHandler(to_handle)]

        return objs

    def generate(self, project):
        self.gen_files = File.fromFiles(self.files)

        for gen_file in self.gen_files:
            gen_file.generate(project)
