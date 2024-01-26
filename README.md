# Projekt TBO

**Skład zespołu:**
- Piotr Bujnowski
- Kacper Kula

Do wykonania procesu CICD użyto aplikacji z laboratoriów - `Flask_Book_Libary`.

## Opis CICD

Do testów wykorzystano skanery:  
  
**SCA**  
- DependencyCheck (dependency-check/Dependency-Check_Action@main)
  
**SAST**  
- Gitleaks (gitleaks/gitleaks-action@v2)
- Bandit
  
**SCA**  
- ZAProxy (zaproxy/action-baseline@v0.10.0)  

  
Aby zaimplementować CICD dodano pliki .yml w folderze .github:

## cicd-build-beta.yml i cicd-build-latest.yml

### **cicd-build-latest.yml**  
Zostaje uruchomiony poprzez operację push oraz pull request, włącza się tylko na gałęzi `master`.

### **cicd-build-beta.yml**  
Zostaje uruchomiony poprzez operację push włącza się tylko na gałęziach innych od master. 

Obie operacje CICD wykonują takie same zadania z tą różnicą, że cicd-build-latest buduje obraz z tagiem latest na branch'u master, a cicd-build-beta buduje obraz z tagiem beta na innych branch'ach.

## Wykonywane zadania:
### **sast-tests** (Run SAST scans (gitleaks | Bandit))  
- *Checkout Repository* (actions/checkout@v4)  
- *Execute gitleaks* (gitleaks/gitleaks-action@v2)  
- *Install Bandit Package* (pip3 install bandit)  
*Run Bandit* (bandit -r --skip B101 .)  

### **dast-tests** (Compose and Run DAST scans (ZAP))  
- *Checkout Repository* (actions/checkout@v4)  
- *Build image* (docker-compose up -d)  
  - buduje aplikacje i uruchamia aplikacje na porcie 8080,  w celu jej przetestowania dla skanów ZAP
*ZAP scans* (zaproxy/action-baseline@v0.10.0)  

### **sca-tests** (Run SCA scans (dependency-check))  
- *Checkout Repository* (actions/checkout@v4)  
- *Run dependency-check* (dependency-check/Dependency-Check_Action@main)  
- *Send Dependency Check Results* (actions/upload-artifact@v2)  
  - wysyła raport skanu do ścieżki `${{ github.workspace }}/reports`  

### **unit-tests**  
- *Set up Python* (actions/setup-python@v4)  
- *Install dependencies*  
- *Test with pytest* (pip install pytest pytest-cov pytest)  

### **build** (Build and push beta image)  
- *Checkout Repository* (actions/checkout@v4)  
- *Login to Docker Hub* (docker/login-action@v3)  
- *Set up Docker Buildx* (docker/setup-buildx-action@v3)  
- *Build and push* (docker/build-push-action@v5)

## Zadanie 2:  
[Pull Request](https://github.com/piotr-bujnowski/projekt-tbo/pull/30) w którym można zobaczyć zmiany. Trzy sztucznie dodane problemy do programu, dwa mocno przykładowe, jeden bardziej realistyczny, wykryte przez Bandita w jobie Run SAST scans (gitleaks):
![](https://i.imgur.com/yAeqWoR.png)
