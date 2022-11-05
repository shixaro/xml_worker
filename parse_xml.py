import configparser
from multiprocessing import Process, Queue
from sources.xml_worker import XML_Worker


def main():
    ConfigFile = 'conf.cfg'
    config = configparser.RawConfigParser()
    config.read(ConfigFile)
    xml_worker = XML_Worker(config)
    xml_data = []
    СSV1_data = {}
    СSV2_data = {}
    files = xml_worker._list_files(config.get("MAIN", "XML_FILES_DIR"))
    for fn in files:
        xml = xml_worker._read_xml_from_zip(fn)
        xml_data.append(xml)

    queue = Queue()
    queue2 = Queue()
    for item in xml_data:
        processes = [Process(target=xml_worker._parse_xml_data, args=(queue, queue2, item,)) for _ in range(4)]
        for p in processes:
            p.start()

        for p in processes:
            p.join()

        СSV1_data = [queue.get() for _ in processes]
        СSV2_data = [queue2.get() for _ in processes]

    with open('file1.csv', 'w') as f:
        for item in СSV1_data:
            for key in item.keys():
                f.write("%s;%s\r\n" % (key,item[key]))


    with open('file2.csv', 'w') as f:
        for xml in СSV2_data:  
            for key in xml.keys():  
                for item in xml[key]:
                    f.write("%s;%s\r\n" % (key,item))

            
if __name__ == '__main__':
    main()
