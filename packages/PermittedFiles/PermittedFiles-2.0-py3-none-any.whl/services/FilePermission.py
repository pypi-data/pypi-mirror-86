"""
    Services FilePermission
    ~~~~~~~~~
Programmer: Phiroj Kumar Dash
Course: CSC540

Theis service checks file type for uploading  feature.
"""
PERMITTED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def permitted_file(filename):
    """
            :param filename: The file name which need to be uploaded
            :return: True, if file type can be uploaded, else false

            Examples:
            >>> permitted_file('upload.pdf')
            True
            >>> permitted_file('upload.txt')
            True
            >>> permitted_file('upload.doc')
            False

     """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in PERMITTED_EXTENSIONS