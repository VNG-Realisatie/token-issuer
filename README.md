# Zaken API Token Issuer #

```yaml
Version: 0.1.0
Source: https://github.com/VNG-Realisatie/token-issuer
Keywords: zaakgericht werken, Tokens
```

## Introductie ##


Ten behoeve van zaakgericht werken is er een nieuwe Tokentool ontwikkeld in fastapi. Deze dient als vervanging voor de bestaande token-tool
om deze binnen VNGr te krijgen.

De werking heeft de GUI achterwege gelaten en werkt nu als een pure restapi. Hierdoor is het aantal endpoints sterk gedaald.


### Werking ###


### Installatie ###


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