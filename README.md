# ZGW Token Issuer

| Key       | Value                                          |
|-----------|------------------------------------------------|
| Version   | 0.1.0                                          |
| Source    | https://github.com/VNG-Realisatie/token-issuer |
| Keywords  | ZGW, tooling                                   |
| Related   | https://github.com/VNG-Realisatie/token-seeder |


## Introductie

Om het zaakgericht werken in de Common Ground architectuuur te ondersteunen zijn de [API's voor Zaakgericht werken ontwikkeld](https://github.com/VNG-Realisatie/gemma-zaken). 
Onderdeel van deze API's is een autorisatie module, de [Autorisaties API](https://github.com/VNG-Realisatie/autorisaties-api) welke tokens gebruikt. 
Deze tokens dienen genereerd en ingericht te worden in de verschillende API's. 

Om de problemen met de bestaande tokentool op te lossen en deze bijvoorbeeld ook op de (nieuwe) testomgeving te laten werken is een nieuwe tokentool ontwikkeld. 
Bijkomend voordeel is dat de nieuwe tokentool nu ook binnen onze eigen omgeving draait.

Deze implementatie heeft de GUI achterwege gelaten en werkt nu als een pure restapi. Hierdoor is het aantal endpoints (en werking) sterk gedaald.

## Swagger en Redoc

Bij de token-issuer is om de werking te vereenvoudigen swagger en redoc documentatie toegevoegd. Deze worden op het standaardadres geserveerd (zie onder).

`{BASE_ADDRESS}` dient vervangen te worden door de instelling van je `ingress` met een port-forward is het meestal `http://localhost:8000`.
Alternatief kan het een dsn record zijn met `https://` zoals `https://zaken-auth.test.vng.cloud`.


#### swagger:

{BASE_ADDRESS}/docs

#### redoc:

{BASE_ADDRESS}/redoc

#### openapi

{BASE_ADDRESS}/api/v1/openapi.json

## Werking

Alvorens de commando's lokaal te draaien is het belangrijk te bepalen van welke omgeving je een token nodig hebt. 

De urls ondersteund door team referentie implementaties zijn:

- test: `https://zaken-auth.test.vng.cloud`
- productie: `https://zaken-auth.vng.cloud`

Wanneer je de token-issuer lokaal draait (bijvoorbeeld in minikube) kan dat een `localhost` zijn maar ook een `ingress` adres zoals beschreven bij _Swagger en Redoc_.

Je kunt eenvoudig het `{BASE_ADDRESS}` vervangen met de volgende commando's

Test:

```shell
export BASE_ADDRESS=https://zaken-auth.test.vng.cloud
```

Productie:

```shell
export BASE_ADDRESS=https://zaken-auth.vng.cloud
```

Onderstaande commando's kunnen ook geplakt worden in API tooling zoals postman of insomnia. 

### Admin token

```shell
curl -L --request POST \
  --url $BASE_ADDRESS/api/v1/register \
  --header 'Content-Type: application/json' \
  --data '{
  "clientIds": [
    "allthescopesarebelongtous222223132532"
  ],
  "label": "user",
  "heeftAlleAutorisaties": true,
  "autorisaties": []
}'
```

### Token met scopes
```shell
curl -L --request POST \
  --url $BASE_ADDRESS/api/v1/register \
  --header 'Content-Type: application/json' \
  --data '{
  "clientIds": [
    "allthescopesarebelongtous222223132532"
  ],
  "label": "user",
  "heeftAlleAutorisaties": false,
  "autorisaties": [
    {
      "component": "zrc",
      "componentWeergave": "Zaken API",
      "scopes": [
        "audittrails.lezen",
        "zaken.aanmaken",
        "zaken.lezen",
        "zaken.verwijderen"
      ],
      "zaaktype": "https://catalogi-api.test.vng.cloud/api/v1/zaaktypen/4f7e14f9-395b-48f2-933c-9fb776b4cdad",
      "maxVertrouwelijkheidaanduiding": "zeer_geheim"
    }
  ]
}
```

### Bestaande secret - id combinatie hergeneren
```shell
curl -L --request POST \
  --url $BASE_ADDRESS/api/v1/tokens \
  --header 'Content-Type: application/json' \
  --data '{
	"client_id": ["sometestwithatoken-I0xPKpr8y0Jx"],
	"secret": "HbQLEs7R6ExBGF66U0e4cSO8YfXAXGOS"
}'
```

## Environmental Variables

Er is een aantal variabelen die te zetten zijn om de werking te bepalen.

| Key                 | Example                                  | Description                                                                |
|---------------------|------------------------------------------|----------------------------------------------------------------------------|
| ENV                 | kubernetes                               | Variabele die bepaalt welke configuratie uit het INI bestand wordt gelezen |
| TOKEN_ISSUER_NAME   | token-issuer-test                        | Variabele die in elke api gezet gaat worden als clientId                   |
| TOKEN_ISSUER_SECRET | supersecretsecret                        | Variabele voor de validatie van de TOKEN_ISSUER_NAME                       |
| ALLOWED_HOSTS       | 'k8s-tokens-local.test,localhost,tokens' | Variabelen die bepalen welke hosts toegestaan worden                       | 


## Scopes

Zoals voorheen via de GUI gebeurde kunnen er ook tokens aangemaakt worden met specifieke scopes. Deze lijst geeft een overzicht.
Het is echter de verantwoording van de consumer om de juiste scopes te gebruiken.

```json
{
  "autorisaties": [
    {
      "component": "ac",
      "componentWeergave": "Autorisaties API",
      "scopes": [
        "autorisaties.bijwerken",
        "autorisaties.lezen"
      ]
    },
    {
      "component": "zrc",
      "componentWeergave": "Zaken API",
      "scopes": [
        "audittrails.lezen",
        "zaken.aanmaken",
        "zaken.bijwerken",
        "zaken.geforceerd-bijwerken",
        "zaken.heropenen",
        "zaken.lezen",
        "zaken.statussen.toevoegen",
        "zaken.verwijderen"
      ],
      "zaaktype": "https://catalogi-api.test.vng.cloud/api/v1/zaaktypen/4f7e14f9-395b-48f2-933c-9fb776b4cdad",
      "maxVertrouwelijkheidaanduiding": "zeer_geheim"
    },
    {
      "component": "ztc",
      "componentWeergave": "Catalogi API",
      "scopes": [
        "audittrails.lezen",
        "zaken.aanmaken",
        "zaken.bijwerken",
        "zaken.geforceerd-bijwerken",
        "zaken.heropenen",
        "zaken.lezen",
        "zaken.statussen.toevoegen",
        "zaken.verwijderen"
      ]
    },
    {
      "component": "drc",
      "componentWeergave": "Documenten API",
      "scopes": [
        "audittrails.lezen",
        "documenten.aanmaken",
        "documenten.bijwerken",
        "documenten.geforceerd-bijwerken",
        "documenten.geforceerd-unlock",
        "documenten.lezen",
        "documenten.lock",
        "documenten.verwijderen",
        "zaken.aanmaken",
        "zaken.bijwerken",
        "zaken.geforceerd-bijwerken",
        "zaken.heropenen",
        "zaken.lezen",
        "zaken.statussen.toevoegen",
        "zaken.verwijderen"
      ],
      "informatieobjecttype": "https://catalogi-api.test.vng.cloud/api/v1/informatieobjecttypen/b3f7c9d7-19e9-46d5-83ca-b13d544ec138",
      "maxVertrouwelijkheidaanduiding": "zeer_geheim"
    },
    {
      "component": "drc",
      "componentWeergave": "Documenten API",
      "scopes": [
        "audittrails.lezen",
        "documenten.aanmaken",
        "documenten.bijwerken",
        "documenten.geforceerd-bijwerken",
        "documenten.geforceerd-unlock",
        "documenten.lezen",
        "documenten.lock",
        "documenten.verwijderen",
        "zaken.aanmaken",
        "zaken.bijwerken",
        "zaken.geforceerd-bijwerken",
        "zaken.heropenen",
        "zaken.lezen",
        "zaken.statussen.toevoegen",
        "zaken.verwijderen"
      ],
      "informatieobjecttype": "https://catalogi-api.test.vng.cloud/api/v1/informatieobjecttypen/10f4a641-61a0-4e9c-8959-9bc1dcafd12d",
      "maxVertrouwelijkheidaanduiding": "zeer_geheim"
    }
  ]
}
```

## Links

* Rapporteer [issues](https://github.com/VNG-Realisatie/token-seeder/issues) bij vragen, fouten of wensen.

## Licentie


Copyright © VNG Realisatie 2023 - 

Licensed under the EUPL


