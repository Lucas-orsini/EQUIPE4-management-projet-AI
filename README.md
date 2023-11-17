# Nutrition Python with Airtable, OpenAI, and Wolfram Alpha

## Project Overview
Ce projet vise à intégrer les données nutritionnelles provenant d'Airtable avec les capacités de traitement du langage naturel de OpenAI (ChatGPT) et les informations nutritionnelles détaillées fournies par Wolfram Alpha. Il automatise la collecte et le traitement des informations sur les macronutriments (lipides, protéines, glucides) pour des calculs nutritionnels précis.

## Features
- Récupération des données sur les macronutriments depuis Airtable.
- Utilisation de OpenAI (ChatGPT) pour obtenir des listes d'aliments basées sur les données de macronutriments.
- Interaction avec Wolfram Alpha pour obtenir des informations nutritionnelles détaillées, y compris le calcul des calories.

## How to Use
1. Configurez vos clés API pour Airtable, OpenAI, et Wolfram Alpha dans le script.
2. Lancez le script pour vérifier les nouveaux enregistrements dans Airtable.
3. Le script envoie des prompts à ChatGPT et récupère les listes d'aliments.
4. Chaque aliment est ensuite envoyé à Wolfram Alpha pour obtenir les informations nutritionnelles.
5. Les résultats sont traités pour obtenir le total des calories.

## Requirements
- Python 3
- Bibliothèques : `requests`, `xml.etree.ElementTree`, `openai`, `airtable`

## Installation
Clonez le dépôt et installez les dépendances requises.
```bash
git clone [URL du dépôt]
cd [Nom du dossier]
pip install [requirement]
