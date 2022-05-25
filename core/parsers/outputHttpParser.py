import re
import pandas as pd
import sys

rx_dict = {
    'first_line': re.compile(r'<---------'),
    'mutation': re.compile(r'(?P<mutate>(.*)mutation(.*))'),
    'status_code': re.compile(r'[^!\s]+\s(?P<status>\d\d\d)\s'),
    'body': re.compile(r'(?P<body>Body.*)(-------->)')
}

def _parse_line(line):
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None

def parse_file(filepath):
        
    data = []
    muta = []
    tot = []
    with open(filepath, 'r',encoding='latin-1') as file_object:
        line = file_object.readline()
        line = file_object.readline()
        while line:
            tot.append(line)
            key, match = _parse_line(line)
            if key == 'first_line':
                if status_code < 400:
                    row = {
                        'Mutation': muta,
                        'Status Code': status_code,
                        'Body': body,
                        'Full Request': "".join(tot)
                    }
                    data.append(row)
                muta = []
                tot = []
            if key == 'mutation':
                mutation = match.group('mutate')
                muta.append(mutation)
#                 print(mutation)
            if key == 'status_code':
                status_code = match.group('status')
                status_code = int(status_code)
#                 print(status_code)
            if key == 'body':
                body = match.group('body')
#                 print(body)
            line = file_object.readline()
        return data


def parse(input_file : str , output_file : str):

    data = parse_file(input_file)
    df=pd.DataFrame(data)
    df.to_csv(output_file)

if __name__ == '__main__':

    if(len(sys.argv) < 3):

        print("./file <input-file> <output-file>")
        exit(0)

    filepath = sys.argv[1]
    data = parse_file(filepath)
    df=pd.DataFrame(data)
    df.to_csv(sys.argv[2])

