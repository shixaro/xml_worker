import os
import jinja2
import random
import string
import time
import xmltodict
from zipfile import ZipFile

class XML_Worker:
	

    def __init__(self, config):
        self._config = config
        self._env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),  self._config.get("MAIN", "TEMPLATES_DIR")  )))
     
        
    def _get_random_string(self, length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string
      
        
    def _generate_random_sequence(self):
        seq = []
        for x in range(random.randrange(1, int(self._config.get("MAIN", "OBJECTS_STRUCT_DEPTH")))):
            seq.append(self._get_random_string(int(self._config.get("MAIN", "RANDOM_STRING_LEN"))))
        return seq
       
        
    def _create_xml_struct(self, sequence):
        t = self._env.get_template(self._config.get("MAIN", "XML_TEMPLATE"))
        data = t.render(random_string = self._get_random_string(int(self._config.get("MAIN", "RANDOM_STRING_LEN"))), 
                        random_number = random.randrange(1, 100),
                        sequence = sequence)
        
        return data
      
        
    def _generate_xml_files(self):
        files = []
        for x in range(int(self._config.get("MAIN", "XMLFILES4ZIP"))):
            filename = "{}/file{}.xml".format(self._config.get("MAIN", "XML_FILES_DIR"), time.time() )
            data = self._create_xml_struct(self._generate_random_sequence())
            f = open(filename, "x")
            f.write(data)
            f.close()
            files.append(filename)
        return files
            
    def _archive_xml_files(self, zipFileName, files):
        zip_path="{}/{}".format(self._config.get("MAIN", "XML_FILES_DIR"), zipFileName)
        zipObj = ZipFile(zip_path, 'w')
        for fn in files:
            zipObj.write(fn, os.path.basename(fn))
    
        zipObj.close()
        
    def _clean_files(self, files):
        for fn in files:
            os.remove(fn) if os.path.exists(fn) else None     
        
        
    def _list_files(self, directory):
        fileslist = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]    
        return fileslist
        
        
    def _read_xml_from_zip(self, zipfile):
        xml_struct = []
        with ZipFile("{}/{}".format(self._config.get("MAIN", "XML_FILES_DIR"), zipfile)) as zf:
            for file in zf.namelist():
                if not file.endswith('.xml'):
                    continue
                else:
                    with zf.open(file) as xmlfile:
                        data = xmltodict.parse(xmlfile.read())

                        xml_struct.append(data)
        return xml_struct
        
    def _test_mp(self, queue):
        num = random.random()
        queue.put(num)
		                 

    def _parse_xml_data(self, queue, queue2, xml_data):
        csv1 = {}
        csv2 = {}
        for item in xml_data:
            (xml_id, xml_level) = (None, None)
            names = []
            xml_id = [r['@value'] for r in item['root']['var'] if r['@name'] == 'id'][0]
            xml_level = [r['@value'] for r in item['root']['var'] if r['@name'] == 'level'][0] 
            if len(item['root']['objects']['object'])>1: 
                names = [r['@name'] for r in item['root']['objects']['object']]
            else: names.append(item['root']['objects']['object']['@name'])


            csv1.update({xml_id: xml_level})
            csv2.update({xml_id: names})

        queue.put(csv1)
        queue2.put(csv2)
