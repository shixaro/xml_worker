import configparser
from sources.xml_worker import XML_Worker


def main():
    ConfigFile = 'conf.cfg'
    config = configparser.RawConfigParser()
    config.read(ConfigFile)
    xml_worker = XML_Worker(config)    
 
    for x in range(int(config.get("MAIN", "ZIP4CREATE"))):
        files = xml_worker._generate_xml_files()
        xml_worker._archive_xml_files("{}.zip".format(x), files) 
        xml_worker._clean_files(files)
		
		
if __name__ == '__main__':
    main()
