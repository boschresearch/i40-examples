# Intro

The purpose of this example is to show how a Digital Product Passport could look like and work with Self Sovereign Identity and Verifiable Credentials.

The content is versy similar to what would be called a Selfdescription / Self-Description in Gaia-X.


# Watch

[Watch the demo - short](https://drive.google.com/file/d/1qdBNwphF0V0ZI82wa5Se9BQsImgR3zyD/view?usp=sharing)

[Watch the demo - a bit longer](https://drive.google.com/file/d/1gRdPqekbplKX68aD2hrzJuNwUd_ihaEk/view?usp=sharing)

# Run

```
DOCKER_BUILDKIT=0 docker-compose up --build
```
`DOCKER_BUILDKIT=0` is required because it does not yet support building images from git subdirs and we need a custom build of acapy for now.


Now open http://localhost:8080/docs#/

# Demo
The API can do more than the demo, but to simplify, the 3 main endpoints are at the very top, tagged with 'Demo'.

Demo result form a provided AAS with a Namplate:
```
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1"
  ],
  "type": "VerifiablePresentation",
  "verifiableCredential": [
    {
      "@context": [
        "https://www.w3.org/2018/credentials/v1",
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
      ],
      "type": [
        "VerifiableCredential",
        "NameplateCredential"
      ],
      "issuer": "did:sov:DuEXo8Ws721z7SDGsyASHK",
      "issuanceDate": "2022-05-13T11:27:12",
      "credentialSubject": {
        "ManufacturerName": "Bosch Rexroth AG",
        "ManufacturerProductDesignation": "Nexo Wi-Fi Cordless Nutrunner",
        "PhysicalAddress": {
          "CountryCode": "DE",
          "Street": "Fornsbacher Straße 92",
          "Zip": "71540",
          "CityTown": "Murrhardt",
          "StateCounty": "Baden-Württemberg"
        },
        "ManufacturerProductFamily": "Cordless Nutrunner",
        "SerialNumber": "917004878",
        "BatchNumber": "",
        "ProductCountryOfOrigin": "DE",
        "YearOfConstruction": "xxxxxxxxxxxxxxxxxxxxxxx",
        "id": "http://boschrexroth.com/shells/0608842005/917004878"
      },
      "proof": {
        "proofPurpose": "assertionMethod",
        "verificationMethod": "did:sov:DuEXo8Ws721z7SDGsyASHK#key-1",
        "type": "Ed25519Signature2018",
        "created": "2022-05-13T11:27:12Z",
        "jws": "eyJhbGciOiAiRWREU0EiLCAiYjY0IjogZmFsc2UsICJjcml0IjogWyJiNjQiXX0..e3LwtEcWGSlg5ldIRoIrO-GSmMEkipXN9jeWnMbR-vR2PdY0cICk6k7R3ulBl0WFJ9J7r1PzwizVSRxGGcHSDQ"
      }
    }
  ],
  "proof": {
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:sov:DuEXo8Ws721z7SDGsyASHK#key-1",
    "type": "Ed25519Signature2018",
    "created": "2022-05-13T11:27:13Z",
    "jws": "eyJhbGciOiAiRWREU0EiLCAiYjY0IjogZmFsc2UsICJjcml0IjogWyJiNjQiXX0..nwvTAtkKR-xB1DxU8gadw0YxIuw9YI6DalHS07-0lcUY4Z5Nfm9KhNKGwD52sbCSBdm5AwHpeProzfNDtUX4Bw"
  }
}
```

The result can be verified with the `/verify` endpoint.

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

# Namplate Submodel Schemas
This is a list of 'Nameplate' schemas we consider valid submodel endpoints we can reuse data from:
```
SEMANTIC_ID_VALUES = [
    'https://admin-shell.io/zvei/nameplate/1/0/Nameplate',
    'https://admin-shell.io/zvei/nameplate/1/0/Nameplate',
    'http://admin-shell.io/Nameplate',
    'https://www.hsu-hh.de/aut/aas/nameplate'
]
```

