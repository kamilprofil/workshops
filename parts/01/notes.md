# Notatki 

## Utworzenie uzytkownikow


Account: 252520820660

k.amilwaldoch.profil - 


```
python management/users.py create --filename data/accounts.csv
```

Nadanie grupy

```
python management/users.py assign_group --filename data/accounts.csv --group fullIamS3 --boundary arn:aws:iam::252520820660:policy/boundary_workshop_01
```





# Ćwiczenia

## 1 Logowanie do konsoli AWS
Link w mailu

## 2 Logowanie uzywając CLI

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html


```
aws configure --profile mojaNazwaProfilu
```

### Uzywanie profili

Podajemy profil jako parametr 
```
aws s3 ls --profil mojaNazwaProfilu
```
przez ustawienie zmiennej środowiskowej:
```
export AWS_PRFILE=mojaNazwaProfilu
```



## 3 Dostęp do S3 

### Z konsoli AWS

### Z CLI

Listowanie bucketów

```
aws s3 ls
```

Listowanie bucketa `wspolny` 
```
aws s3 ls s3://[nazwa]
```

### Pobieranie pliku


Pobierzmy plik:

``` ekipa.jpeg ```

Pobierzmy plik:

```lista-plac-profil.jpg```

### Przegląd policy  dla bucketa `wspolny`
### Policy simulator
Sprawdźmy:
- dostęp do wybranego serwisu(w konsoli kliknij Services na górnym pasku)
- dostęp do IAM
- dostęp do S3
- dostęp do S3 do bucketa wspolny
- dostęp do S3 do bucketa wspolny, plik lista-plac-profil.jpg

### Wlasny bucket
- utwórz bucket
- wrzuć jeden plik bezpośrednio
- wrzuć jeden plik do "folderu" w buckecie
- sprawdź dostęp z konsoli - ls, ls w folderze
    _(powinno być dostępne od razu - S3 oferuje Strong  read-after-write Consistency)_


## Tworzymy nowego uytkownika 
- stwórz nowego uytkownika(IAM) 
- zachowaj hasło, pobierz plik z access key i secret key
- w trybie incognito zaloguj się na nowe konto
### Permission boundaries
- utwórz grupę i nadaj uprawnienia do dowolnego resource(w konsoli kliknij Services na górnym pasku)
- wejdź na ten serwis(w konsoli kliknij Services na górnym pasku) - co widać? (Boundaries)

# Tworzenie uprawnień 
- utwórz nowy profil z konsoli i sprawdź listę bucketów (`ls`)






# Hostowanie strony WWW z S3


Z poziomu terminala, wgraj do bucketa jakiś dokument html, na przykład:

https://github.com/giotsere/minimalist-portfolio

Do wgrania uzyj komendy `cp`


- Wejdź w properties  - static website hosting
- Otwórz utworzony adres.
- brak dostepu?
- odblokowujemy block access
- w permissions dodajmy nową policy(mozna przez kreator):
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::[mybucket]/*"
        }
    ]
}
```
