# OWL to TPTP: Translation Steps

## Preparatory Installations (if necessary)
```
$ sudo apt-get install 
$ sudo apt-get -y install openjdk-19-jre-headless
$ sudo apt-get -y install maven
$ sudo apt-get -y install python3
$ sudo apt-get -y install pip
$ pip install gavel
$ pip install gavel_owl
$ pip install py4j
$ pip install ply
```

## Clone Repositories
Clone the repositories 'lkif-core' and 'python-gavel-owl' from GitHub.

```
$ git clone https://github.com/RinkeHoekstra/lkif-core.git
$ git clone https://github.com/gavel-tool/python-gavel-owl.git
```


## Modify ApiServer.java
Modify the file './python-gavel-owl/java/src/main/java/translation/ApiServer.java' by replacing the method 'translateOntologyFromFile' in line 241. The new code is the following:

```
    public AnnotatedLogicElement[] translateOntologyFromFile(String path) throws Exception {
        System.out.println("Starting Translation");
        
        File file = new File(path);
        File folder = new File(file.getParent());
        org.semanticweb.owlapi.util.AutoIRIMapper mapper = new org.semanticweb.owlapi.util.AutoIRIMapper(folder, false);
        
        OWLOntologyManager manager = OWLManager.createOWLOntologyManager();
        manager.addIRIMapper(mapper);
        
        OntologyTranslator translator = new OntologyTranslator(
            manager.loadOntologyFromOntologyDocument(file), false);
        return translator.translate().toArray(new AnnotatedLogicElement[0]);
    }
```

The modification allows the ontology manager to consider referenced files in the same directory.


## Modify cli.py

Modify the file './python-gavel-owl/src/gavel_owl/cli.py' by replacing the first three lines (39-42) of the method 'start_server' in line. The new code is the following:

```
def start_server(jp, pp):
    """Start a server listening to ports `jp` and `pp`"""
    packdir = "."
    p = subprocess.Popen(['java', '-Xmx2048m', '-jar', os.path.join(packdir, 'jars', 'api.jar'), jp, pp],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
```

The modification makes the server be executed in the correct directory.


## Build Java Project

```
$ cd ./python-gavel-owl/java
$ mvn install
$ cp ./target/java-1.0-SNAPSHOT.one-jar.jar ../src/gavel_owl/jars/api.jar
$ cd ../..
```


# Start Server

```
$ cd ./python-gavel-owl/src/gavel_owl
$ python3 -c 'from cli import start_server; start_server()'
$ cd ../../..
```


# Execute Translation

```
$ python3 -m gavel translate owl tptp ./lkif-core/lkif-core.owl > ./lkif-core.ax
```


# Stop Server

```
$ cd ./python-gavel-owl/src/gavel_owl
$ python3 -c 'from cli import stop_server; stop_server()'
```


# Optional: Shorten Axiom Names

Replace all occurrences of 'http___www_estrellaproject_org_' in the generated lkif-core.ax with an empty string in order to shorten the axiom names.

