# grp12_Wario_Mouchet-Mouchet-Tan

### Installation

Afin de pouvoir tester l'application et le jeu fait sur Unity il faut clone le projet du dépôt git (lien du dépot).

Ensuite, depuis Unity Hub il faut aller dans "open -> open project from disk" et selectionner le folder Coding in Flow 2D Project. L'importation peut prendre plusieurs longues minutes.
Une fois l'importation terminée il faut sélectionner la scène "Project Compilateur.unity", les tests peuvent se faire en lançant la simulation (bouton play).

Les différentes extensions de python nécessaires aux fonctionnement du compilateur sont :

- Yacc
- PLY
- Pydot
- Graphviz

Une fois toutes les extensions installées et le projet Unity mis en place il est possible d'exécuter la compilation avec la commande "python compiler.py <nomdelinput>.txt" depuis le folder du projet.

Celui ci modifiera directement le fichier .unity de notre scène, il faudra uniquement reload la scène sur Unity.
