## Réponses tp

# Analyse rapport "report.html"

aucun tests ne sont passés, il y a 4erreurs :
(test_page_loads, test_addition, test_division_by_zero, test_all_operations sont tous en Error, pas en Failed).

Les 4 erreurs viennent toutes du setup.

La cause commune est un problème d’initialisation du driver Selenium (ChromeDriver) :
OSError: [Errno 8] Exec format error sur un fichier THIRD_PARTY_NOTICES.chromedriver fourni par webdriver-manager.
=> problème d'environnement/config driver.