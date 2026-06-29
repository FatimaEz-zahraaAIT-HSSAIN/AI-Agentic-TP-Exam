# Agent Chef Personnel

Un chef personnel interactif propulsé par l'IA, construit avec **Langchain**, **Ollama**, et **Langgraph**. Cet agent agit comme votre assistant culinaire intelligent : il prend note des ingrédients dans votre réfrigérateur, mémorise vos préférences alimentaires tout au long de la conversation, et effectue des recherches sur le web pour trouver les meilleures recettes et techniques culinaires afin de vous proposer des plats sur mesure.

## Fonctionnalités

* **Chat interactif :** Communiquez avec l'agent de manière fluide et en langage naturel.
* **Mémoire conversationnelle :** Utilise `InMemorySaver` pour se souvenir de vos restrictions alimentaires (ex : végétarien, allergies) et de vos préférences tout au long de la session.
* **Capacité de recherche Web :** Intègre le `TavilyClient` comme outil personnalisé, permettant à l'agent de naviguer sur Internet pour trouver des recettes récentes et des associations d'ingrédients.
* **Traitement IA local :** S'exécute entièrement en local via **Ollama** (`llama3.2:3b`), garantissant le respect de votre vie privée et une utilisation gratuite sans coût de tokens.

---

## Prérequis

Avant de lancer le projet, assurez-vous d'avoir installé les éléments suivants :

1.  **Python 3.8+**
2.  **Ollama :** Téléchargez et installez-le depuis [ollama.com](https://ollama.com/).
3.  **Modèle Llama 3.2 :** Une fois Ollama installé, ouvrez votre terminal et téléchargez le modèle requis en exécutant cette commande :
    ```bash
    ollama run llama3.2:3b
    ```
4.  **Clé API Tavily :** Obtenez une clé API gratuite pour la recherche web sur [Tavily](https://tavily.com/).

---

## Installation et Configuration

**1. Accéder au dossier du projet**
Naviguez vers le dossier contenant votre script :
```bash
cd chemin/vers/votre/projet
```

**2. Créer un environnement virtuel**
Il est fortement recommandé d'utiliser un environnement virtuel pour gérer les dépendances :
```bash
python -m venv .venv
```

**3. Activer l'environnement virtuel**
* **Windows (PowerShell) :**
    ```powershell
    .\.venv\Scripts\Activate.ps1
    ```
* **Mac/Linux :**
    ```bash
    source .venv/bin/activate
    ```

**4. Installer les dépendances**
Assurez-vous que votre environnement virtuel est bien activé, puis installez les bibliothèques nécessaires :
```bash
python -m pip install langchain langchain-ollama tavily-python python-dotenv langgraph
```

**5. Configurer les variables d'environnement**
Créez un fichier nommé `.env` à la racine de votre projet et ajoutez-y votre clé API Tavily :
```env
TAVILY_API_KEY=votre_vraie_cle_api_ici
```

---

## Utilisation

Assurez-vous que l'application Ollama est ouverte et s'exécute en arrière-plan. Ensuite, lancez le script depuis votre terminal :

```bash
python chef-agent.py
```

### Exemple d'interaction

![Output](./assets/Chef-Output.png)

---

## 🛠️ Construit avec

* [Langchain](https://python.langchain.com/) - Framework pour le développement d'applications LLM.
* [Ollama](https://ollama.com/) - Exécuteur local de LLM.
* [Tavily](https://tavily.com/) - Moteur de recherche optimisé pour les agents IA.
* [Langgraph](https://python.langchain.com/docs/langgraph/) - Utilisé pour la gestion de l'état et de la mémoire conversationnelle.