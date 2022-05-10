# Intro

The purpose of this example is to show how a Digital Product Passport could look like and work with Self Sovereign Identity and Verifiable Credentials.

The content is versy similar to what would be called a Selfdescription / Self-Description in Gaia-X.


# Watch
[Watch the demo](https://drive.google.com/file/d/1gRdPqekbplKX68aD2hrzJuNwUd_ihaEk/view?usp=sharing)

# Run

## Acapy / Wallet
```
DOCKER_BUILDKIT=0 docker-compose up --build
```
`DOCKER_BUILDKIT=0` is required because it does not yet support building images from git subdirs and we need a custom build of acapy for now.

## The API endpoint
```
# install
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt

# run
python main.py
```
and open http://localhost:8080/docs#/

# Demo
The API can do more than the demo, but to simplify, the 2 main endpoints are at the very top, tagged with 'Demo'.

Demo result form a provided AAS with a Namplate:
```

```

# Background
The system creates a Verifiable Credential (VC) and puts it into a Verifiable Presentation (VP).

For this, we introduce a new context to work with the `nameplate` schema.
```
{
    "aio": "https://admin-shell-io.com/ns#",
    "NameplateCredential": "aio:NameplateCredential",
    "ManufacturerName": "aio:ManufacturerName",
    "ManufacturerProductDesignation": "aio:ManufacturerProductDesignation",
    "PhysicalAddress": "aio:PhysicalAddress",
    "CountryCode": "aio:CountryCode",
    "Street": "aio:Street",
    "Zip": "aio:Zip",
    "CityTown": "aio:CityTown",
    "StateCounty": "aio:StateCounty",
    "ManufacturerProductFamily": "aio:ManufacturerProductFamily",
    "SerialNumber": "aio:SerialNumber",
    "BatchNumber": "aio:BatchNumber",
    "ProductCountryOfOrigin": "aio:ProductCountryOfOrigin",
    "YearOfConstruction": "aio:YearOfConstruction"
}
```

The 'Nameplate' is the schema defined as part of 'Plattform i40' and can be found here:

https://www.plattform-i40.de/IP/Redaktion/DE/Downloads/Publikation/Submodel_Templates-Asset_Administration_Shell-digital_nameplate.html


