# SETUP

To set up a candig-server, you may follow the following instructions.

You can run the ingestion and test a server with the resulting repo as follows 
(requires Python 2.7 for candig-server<1.0.0, or Python 3.6 for candig-server>=1.0.0, note that Python 3.7 is not currently supported.)

.. code:: bash

    # Install
    virtualenv test_server # If you are running Python 2
    python3 -m venv test_server # If you are running Python 3.6
    
    cd test_server
    source bin/activate
    pip install --upgrade pip setuptools
    pip install candig-server # Specify anything <1.0.0 for Python 2.7, or >=1.0.0 for Python 3.6.
    pip install candig-ingest

    # ingest data and make the repo
    mkdir candig-example-data
    ingest candig-example-data/registry.db <path to example data, like: mock_data/clinical_metadata_tier1.json>

    # optional
    # add peer site addresses
    candig_repo add-peer candig-example-data/registry.db <peer site IP address, like: http://127.0.0.1:8001>

    # optional
    # create dataset for reads and variants
    candig_repo add-dataset --description "Reads and variants dataset" candig-example-data/registry.db read_and_variats_dataset

    # optinal
    # add reference set, data source: https://www.ncbi.nlm.nih.gov/grc/human/ or http://genome.wustl.edu/pub/reference/
    candig_repo add-referenceset candig-example-data/registry.db <path to downloaded reference set, like GRCh37-lite.fa> -d "GRCh37-lite human reference genome" --name GRCh37-lite --sourceUri "http://genome.wustl.edu/pub/reference/GRCh37-lite/GRCh37-lite.fa.gz"

    # optional
    # add reads
    candig_repo add-readgroupset -r -I <path to bam index file> -R GRCh37-lite candig-example-data/registry.db read_and_variats_dataset <path to bam file>

    # optional
    # add variants
    candig_repo add-variantset -I <path to variants index file> -R GRCh37-lite candig-example-data/registry.db read_and_variats_dataset <path to vcf file>
    
    # optional
    # add sequence ontology set
    # wget https://raw.githubusercontent.com/The-Sequence-Ontology/SO-Ontologies/master/so.obo
    candig_repo add-ontology candig-example-data/registry.db <path to sequence ontology set, like: so.obo> -n so-xp

    # optional
    # add features/annotations
    #
    ## get the following scripts
    # https://github.com/ga4gh/ga4gh-server/blob/master/scripts/glue.py
    # https://github.com/ga4gh/ga4gh-server/blob/master/scripts/generate_gff3_db.py
    #
    ## download the relevant annotation release from Gencode
    # https://www.gencodegenes.org/releases/current.html
    #
    ## decompress
    # gunzip gencode.v27.annotation.gff3.gz
    #
    ## build the annotation database
    # python generate_gff3_db.py -i gencode.v27.annotation.gff3 -o gencode.v27.annotation.db -v    
    #
    # build index for your annotation database
    # Run "CREATE INDEX name_type_index ON FEATURE (gene_name, type)" in Sqlite browser
    #
    # add featureset
    candig_repo add-featureset candig-example-data/registry.db read_and_variats_dataset <path to the annotation.db> -R GRCh37-lite -O so-xp

    # optional
    # add phenotype association set from Monarch Initiative
    # wget http://nif-crawler.neuinfo.org/monarch/ttl/cgd.ttl
    candig_repo add-phenotypeassociationset candig-example-data/registry.db read_and_variats_dataset <path to the folder containing cdg.ttl>

    # optional
    # add disease ontology set, like: NCIT
    # wget http://purl.obolibrary.org/obo/ncit.obo
    candig_repo add-ontology -n NCIT candig-example-data/registry.db ncit.obo

    # launch the server at different IP and/or port:
    candig_server --host 127.0.0.1 --port 8000 -c NoAuth


    http://127.0.0.1:8000/


and then, from another terminal:

.. code:: bash

    curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' \
        http://127.0.0.1:8000/datasets/search \
        | jq '.'

giving:

.. code:: JSON

    {
      "datasets": [
        {
          "description": "PROFYLE test metadata",
          "id": "WyJQUk9GWUxFIl0",
          "name": "PROFYLE"
        }
      ]
    }

