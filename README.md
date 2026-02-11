# Réponses tp

# Analyse rapport report.html

4 erreurs, tous les tests en Error pas Failed. Erreurs au setup seulement.
Cause : OSError Exec format error sur THIRD_PARTY_NOTICES.chromedriver (webdriver-manager). Problème env / driver.

# Erreurs et changements

# pip introuvable

command not found pip → utiliser python3 -m pip

# ChromeDriver Exec format error

webdriver-manager mauvais fichier. Changement : plus de ChromeDriverManager, utiliser Selenium Manager (webdriver.Chrome(options=options) sans Service).

# test_decimal_numbers vide ou Timeout

get_result lisait trop tôt → attendre que result ait du texte.
Navigateur refusait décimales (input number sans step = entiers). Changement : step="any" sur les deux input number dans index.html.

# Lancer les tests

cd tests
python3 -m pip install -r requirements.txt
python3 -m pytest -v

Firefox : BROWSER=firefox python3 -m pytest -v

# Avantages

Moins de tests manuels répétitifs.
Rapports automatiques (html, couverture).

# CI/CD et qualité

Tests lancés à chaque vpush et PR
Erreur dans  GitHub Actions.
Main reste plus propre grâce à la PR depuis develop
# Défis Selenium

Problème de driver Chrome sur macOS
Gestion des navigateurs différents.

# Améliorer la stabilité

Attendre éléments WebDriverWait
Isoler la l ogique dans Object

# Métriques importantes


Nombre de tests passés / échoués.
Temps d exécution de la suite de tests.

# Efficacité du pipeline CI/CD

Temps moyen d un run run Actions.
Nombre de builds rouges  peut corrigés rapidemen
