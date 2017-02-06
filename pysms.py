import urllib3
import base64
import xml.etree.ElementTree as ET
import csv
import xml.dom.minidom as XML

class Session:

    def __init__(self, host, user, pwd, request):
        self.http = urllib3.PoolManager()
        self.headers = self.headers(user, pwd)
        self.requestUrl = self.requestUrl(host)
        if self.requestUrl:
            self.request = self.http.request('POST', self.requestUrl, body=request, headers=self.headers)

    def headers(self, user, pwd):
        base64string = base64.encodestring('%s:%s' % (user, pwd)).replace('\n','')
        headers = {
        'Authorization' : 'Basic %s' % base64string,
        'Content-type' : 'application/xml'
        }
        return headers

    def requestUrl(host):
        return 'https://' + host + ':443/smsxml/SystemManagementService.php'

class XmlDocument:

    def __init__(self, sessionID):
        self.rootTag = ET.Element('soapenv:Envelope')
        self.rootTag.set('xmlns:soapenv', 'http://schemas.xmlsoap.org/soap/envelope/')
        self.rootTag.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
        self.rootTag.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        self.headerTag = ET.SubElement(self.rootTag, 'soapenv:Header')
        self.sessionIdTag = ET.SubElement(self.headerTag, 'ns1:sessionID')
        self.sessionIdTag.set('soapenv:actor', 'http://schemas.xmlsoap.org/soap/actor/next')
        self.sessionIdTag.set('soapenv:mustUnderstand', '1')
        self.sessionIdTag.set('xsi:type', 'xsd:string')
        self.sessionIdTag.set('xmlns:ns1', 'http://xml.avaya.com/ws/session')
        if sessionID is not None:
            self.sessionIdTag.text = sessionID
        self.bodyTag = ET.SubElement(self.rootTag, 'soapenv:Body')
        self.submitRequestTag = ET.SubElement(self.bodyTag, 'ns2:submitRequest')
        self.submitRequestTag.set('xmlns:ns2', 'http://xml.avaya.com/ws/SystemManagementService/2008/07/01')
        self.submitRequestTag.set('xmlns:ns3', 'http://xml.avaya.com/ws/session')
        self.modelFields = ET.SubElement(self.submitRequestTag, 'modelFields')

    def displayStation(self, extension):

        self.StationTag = ET.SubElement(self.modelFields, 'Station')
        self.operationTag = ET.SubElement(self.submitRequestTag, 'operation')
        self.operationTag.text = 'display'
        self.objectNameTag = ET.SubElement(self.submitRequestTag, 'objectname')
        self.qualifierTag = ET.SubElement(self.submitRequestTag, 'qualifier')
        self.qualifierTag.text = extension

class SMS:

    def __init__(self, host, user, pwd, sessionID=None):
        if sesssionID is not None:
            self.xml = XmlDocument(sessionID)
            self.sessionID = sessionID
            self.user = user
            self.pwd = pwd
            self.host = host
        else:
            self.xml = XmlDocument()
    def getLines(self, extension):
        self.xml.displayStation(extension)
        xmlDoc = self.xml.rootTag
        xmlDoc = ET.tostring(xmlDoc)
        session = ClientSession(self.host, self.user, self.pwd, xmlDoc)
        self.response = ET.fromstring(session.request.data)
        self.extension = [extension.text for extension in self.response.iter('Extension')]
        self.sharedLines = [shared.text for shared in self.response.iter('Button_Data_3')]
        self.allLines = list(set(self.extension + self.sharedlines))
