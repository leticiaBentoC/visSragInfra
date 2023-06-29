#!/bin/bash

mkdir -p dados
curl https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SRAG/2020/INFLUD20-01-05-2023.csv -o dados/srag_2020.csv
curl https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SRAG/2021/INFLUD21-01-05-2023.csv -o dados/srag_2021.csv
curl https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SRAG/2022/INFLUD22-03-04-2023.csv -o dados/srag_2022.csv
curl https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SRAG/2023/INFLUD23-29-05-2023.csv -o dados/srag_2023.csv

