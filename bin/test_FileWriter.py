import pytest
import json
import os
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader 

# Do some funny business to load the modules from a file without the .py extension
# see https://stackoverflow.com/a/43602645
from importlib.util import spec_from_loader, module_from_spec
from importlib.machinery import SourceFileLoader

spec = spec_from_loader("pagurus", SourceFileLoader("pagurus", "./pagurus"))
pagurus=module_from_spec(spec)
spec.loader.exec_module(pagurus)

def test_FileWriter_csv(tmp_path):
    print("Output file path", tmp_path)
    header = ['name1',"name2","name3"]
    outfile = tmp_path/f"test.csv"
    fw = pagurus.FileWriter(outfile=outfile, header=header,write_header=True)
    assert( fw.header == header)
    assert( fw.write_header == True)
    assert( fw.outfile == outfile)
    assert( outfile.is_file())
    fw.write(0,1,2)
    fw.close()
    with open(outfile) as f:
        contents = f.read()
        print(contents)
        lines = contents.splitlines()
        assert( lines[0] == ",".join(header))
        assert( lines[1] == "0,1,2")
    fw.outfile.unlink()

def test_FileWriter_csv_envvar(tmp_path):
    print("Output file path", tmp_path)
    header = ['name1',"name2","name3"]
    outfile = tmp_path/f"test.csv"

    # Clear out environment variables we will be testing with
    try:
        os.environ.pop("testytesty")
        os.environ.pop("testytoasty")
    except:
        pass
    os.environ['testytesty'] = 'test'
    os.environ['testytoasty'] = 'test2'
    fw = pagurus.FileWriter(outfile=outfile, header=header,write_header=True,env=["testytesty","testytoasty"])
    header2 = header+["testytesty","testytoasty"]

    assert( fw.header == header2)
    assert( fw.write_header == True)
    assert( fw.outfile == outfile)
    assert( outfile.is_file())
    fw.write(0,1,2,"test","test2")
    fw.close()
    with open(outfile) as f:
        contents = f.read()
        print(contents)
        lines = contents.splitlines()
        assert( lines[0] == ",".join(header2))
        assert( lines[1] == '0,1,2,test,test2')
    fw.outfile.unlink()


def test_FileWriter_json(tmp_path):
    print("Output file path", tmp_path)
    header = ['name1',"name2","name3"]
    outfile = tmp_path/f"test.json"
    fw = pagurus.FileWriter(outfile=outfile, header=header,write_header=True,jsonout=True)
    assert( fw.header == header)
    assert( fw.write_header == False)
    assert( fw.outfile == outfile)
    assert( outfile.is_file())
    fw.write(0,1,2)
    fw.close()
    with open(outfile) as f:
        contents = f.read()
        print(contents)
        lines = contents.splitlines()
        jsonout = json.dumps(dict(zip(header,[0,1,2])))
        assert( lines[0] == jsonout)
    fw.outfile.unlink()

def test_FileWriter_json_envvar(tmp_path):
    print("Output file path", tmp_path)
    header = ['name1',"name2","name3"]
    outfile = tmp_path/f"test.json"

    # Clear out environment variables we will be testing with
    try:
        os.environ.pop("testytesty")
        os.environ.pop("testytoasty")
    except:
        pass
    with pytest.raises(KeyError) as e:
        fw = pagurus.FileWriter(outfile=outfile, header=header,write_header=True,jsonout=True,env=["testytesty","testytoasty"])
    os.environ['testytesty'] = 'test'
    os.environ['testytoasty'] = 'test2'
    fw = pagurus.FileWriter(outfile=outfile, header=header,write_header=True,jsonout=True,env=["testytesty","testytoasty"])
    header2 = header+["testytesty","testytoasty"]

    assert( fw.header == header2)
    assert( fw.write_header == False)
    assert( fw.outfile == outfile)
    assert( outfile.is_file())
    fw.write(0,1,2,"test","test2")
    fw.close()
    with open(outfile) as f:
        contents = f.read()
        print(contents)
        lines = contents.splitlines()
        jsonout = json.dumps(dict(zip(header2,[0,1,2,"test","test2"])))
        assert( lines[0] == jsonout)
    fw.outfile.unlink()


