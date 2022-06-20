# 01 notes

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

# 1 Logowanie do konsoli AWS
Link w mailu

# 2 Logowanie uzywając CLI

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html


```
aws configure --profile mojaNazwa
```




