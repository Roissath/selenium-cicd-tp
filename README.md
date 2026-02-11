# TP Selenium et CI/CD

Application web calculatrice avec tests Selenium automatisés.

## Installation

```bash
cd tests
pip install -r requirements.txt
```

## Exécution des tests

```bash
python3 -m pytest test_selenium.py -v
```

## Structure

- `src/` : Application web (HTML, CSS, JS)
- `tests/` : Tests Selenium avec Page Object Pattern
- `.github/workflows/` : Pipeline CI/CD GitHub Actions

---

## Réflexion

### 1. Avantages observés

**Automatisation des tests :**
- Détection rapide des régressions à chaque push
- Tests reproductibles dans un environnement contrôlé
- Gain de temps comparé aux tests manuels

**CI/CD et qualité du code :**
- Feedback instantané via GitHub Actions
- Empêche le merge de code défectueux
- Historique des tests dans les artifacts

### 2. Défis rencontrés

**Difficultés avec Selenium :**
- Problèmes de compatibilité WebDriver
- Nécessité d'attentes explicites pour éviter les erreurs
- Tests instables selon le temps de chargement

**Améliorations de stabilité :**
- Utiliser des attentes explicites (`WebDriverWait`)
- Mode headless en CI pour plus de stabilité
- Isolation des tests (rechargement de page)

### 3. Métriques importantes

**Métriques projet :**
- Taux de réussite des tests
- Temps d'exécution du pipeline
- Nombre de tests

**Mesurer l'efficacité CI/CD :**
- Temps de feedback (délai entre push et résultat)
- Fréquence de déploiement
- Taux d'échec du pipeline

---

## Ressources

- [Documentation Selenium](https://selenium-python.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Best Practices pour les tests Selenium](https://www.selenium.dev/documentation/test_practices/)
