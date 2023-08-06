'''
Copyright (c) 2020 by Windward Studios, Inc. All rights reserved.
This software is the confidential and proprietary information of
Windward Studios ("Confidential Information").  You shall not
disclose such Confidential Information and shall use it only in
accordance with the terms of the license agreement you entered into
with Windward Studios, Inc.
'''

import six
from windwardrestapi.Model import ImportMetrics

'''
A generated document. Also used as a pending document generation job where just the Guid and Tag properties are set.
'''
class Document(object):

    attributeMap = {
        'guid': 'Guid',
        'data': 'Data',
        'pages': 'Pages',
        'numberOfPages': 'NumberOfPages',
        'tag': 'Tag',
        'importInfo': 'ImportInfo',
        'errors': 'Errors'
    }

    '''
    Creates a new instance of the document class object.
    '''
    def __init__(self, guid=None, data=None, pages=None, numberOfPages=None, tag=None, importInfo=None, errors=None):

        self._guid = None
        self._data = None
        self._pages = None
        self._numberOfPages = None
        self._tag = None
        self._importInfo = []
        self._errors = None
        # self.discriminator = None
        if guid is not None:
            self.guid = guid
        if data is not None:
            self.data = data
        if pages is not None:
            self.pages = pages
        if numberOfPages is not None:
            self.numberOfPages = numberOfPages
        if tag is not None:
            self.tag = tag
        if importInfo is not None:
            self.importInfo = importInfo
        if errors is not None:
            self.errors = errors

    @property
    def guid(self):
        """Gets the guid of this Document.

        The unique identifier for this request.

        :return: The guid of this Document.
        :rtype: str
        """
        return self._guid

    @guid.setter
    def guid(self, guid):
        """Sets the guid of this Document.

        The unique identifier for this request.  # noqa: E501

        :param guid: The guid of this Document.  # noqa: E501
        :type: str
        """

        self._guid = guid

    @property
    def data(self):
        """Gets the data of this Document.

        The generated document as a single file in the user specified format. If this is populated Pages will be null.

        :return: The data of this Document.
        :rtype: str
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this Document.

        The generated document as a single file in the user specified format. If this is populated Pages will be null.

        :param data: The data of this Document.
        :type: str
        """

        self._data = data

    @property
    def pages(self):
        """Gets the pages of this Document.

        The generated document as a distinct file per page in the user specified format. If this is populated Data will be null. This is produced by the image document generator and by the HTML document generator when it is in per page mode.

        :return: The pages of this Document.
        :rtype: str
        """
        return self._pages

    @pages.setter
    def pages(self, pages):
        """Sets the pages of this Document.

        The generated document as a distinct file per page in the user specified format. If this is populated Data will be null. This is produced by the image document generator and by the HTML document generator when it is in per page mode.

        :param pages: The pages of this Document.
        :type: str
        """

        self._pages = pages

    @property
    def numberOfPages(self):
        """Gets the number_of_pages of this Document.

        The number of pages in the generated document.

        :return: The number_of_pages of this Document.
        :rtype: int
        """
        return self._numberOfPages

    @numberOfPages.setter
    def numberOfPages(self, number_of_pages):
        """Sets the number_of_pages of this Document.

        The number of pages in the generated document.

        :param number_of_pages: The number_of_pages of this Document.
        :type: int
        """

        self._numberOfPages = number_of_pages

    @property
    def tag(self):
        """Gets the tag of this Document.

        Anything you want. This is passed in to the repository & job handlers and is set in the final generated document object. The RESTful engine ignores this setting, it is for the caller's use.

        :return: The tag of this Document.
        :rtype: str
        """
        return self._tag

    @tag.setter
    def tag(self, tag):
        """Sets the tag of this Document.

        Anything you want. This is passed in to the repository & job handlers and is set in the final generated document object. The RESTful engine ignores this setting, it is for the caller's use.

        :param tag: The tag of this Document.
        :type: str
        """

        self._tag = tag

    @property
    def importInfo(self):
        """Gets the import_info of this Document.

        The info on each import processed generating the document. The list is populating only if the ImportInfo enabled.
        :return: The import_info of this Document.
        :rtype: list[ImportMetrics]
        """
        return self._importInfo

    @importInfo.setter
    def importInfo(self, import_info):
        """Sets the import_info of this Document.

        The info on each import processed generating the document. The list is populating only if the ImportInfo enabled.

        :param import_info: The import_info of this Document.
        :type: list[ImportMetrics]
        """
        for item in import_info:
            print(item)
            type = item["Type"]
            tag = item["Tag"]
            filename = item["Filename"]
            children = item["Children"]

            self._importInfo.append(
                ImportMetrics.ImportMetrics(type=type, tag=tag, filename=filename, children=children))

    @property
    def errors(self):
        """Gets the errors of this Document.  # noqa: E501

        Contains a list of issues (errors and warnings) found during the document generation. The list is populating only if the error handling and verify is enabled.

        :return: The errors of this Document.  # noqa: E501
        :rtype: list[Issue]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this Document.

        Contains a list of issues (errors and warnings) found during the document generation. The list is populating only if the error handling and verify is enabled.

        :param errors: The errors of this Document.
        :type: list[Issue]
        """

        self._errors = errors

    def toDict(self):
        responseDict = {}
        for key, value in six.iteritems(self.attributeMap):
            tempVal = getattr(self, key)
            if tempVal is None:
                pass
            elif isinstance(tempVal, (str, int, dict)):
                responseDict.update({value: tempVal})
            elif isinstance(tempVal, list):
                responseDict.update({value: []})
                for item in tempVal:
                    if isinstance(item, (str, int, dict)):
                        responseDict.update({value: tempVal})
                    else:
                        responseDict[value].append(item.toDict())
            else:
                responseDict.update({value: tempVal.toDict()})
        return responseDict