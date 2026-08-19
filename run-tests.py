import os
import subprocess
import sys

# 1. Détection du projet
if os.path.exists("vite.config.ts"):
	print("Projet Front-end détecté")
	project_type = "front"
elif os.path.exists("nest-cli.json"):
	print("Projet Back-end détecté")
	project_type = "back"
else:
	print("Type de projet inconnu")
	exit()

# 2. Vérification des dépendances
if not os.path.exists("node_modules"):
	install_result = subprocess.run(["npm", "ci"])
	if install_result.returncode != 0:
		print("Erreur lors de l'installation des dépendances")
		sys.exit(1)

# 3. Nettoyer les anciens résultats de test
if os.path.exists("test-results"):
	subprocess.run(["rm", "-rf", "test-results"])

# 4. Exécution des tests
if project_type == "front":
	result = subprocess.run(["npm", "run", "test"])
	end_result = result.returncode
else:
	result_global = subprocess.run(["npm", "run", "test"])
	result_e2e = subprocess.run(["npm", "run", "test:e2e", "--", "--passWithNoTests"])
	end_result = result_global.returncode + result_e2e.returncode

# 5. Vérification des résultats de test

if end_result == 0: 
	print("Tests réussis")
else:
	print("Tests échoués")

# 6. Code de sortie
if end_result  == 0:
	sys.exit(0)
else:
	sys.exit(1)

