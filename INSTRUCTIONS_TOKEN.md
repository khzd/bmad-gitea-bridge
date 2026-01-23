# Comment générer un nouveau token Gitea

## Étapes à suivre:

1. **Connectez-vous à Gitea**
   - URL: http://192.168.0.76:3000
   - Utilisez vos identifiants admin

2. **Accédez aux paramètres**
   - Cliquez sur votre avatar (en haut à droite)
   - Sélectionnez "Paramètres" ou "Settings"

3. **Générez un token**
   - Allez dans l'onglet "Applications"
   - Section "Gérer les jetons d'accès" / "Manage Access Tokens"
   - Cliquez sur "Générer un nouveau jeton" / "Generate New Token"

4. **Configurez le token**
   - Nom: `bmad-gitea-bridge`
   - Permissions requises:
     - ✅ repo (toutes les permissions repository)
     - ✅ admin:org (si vous utilisez des organisations)
     - ✅ user (lecture/écriture utilisateurs)
     - ✅ issue (création/modification issues)

5. **Copiez le token**
   - ⚠️ IMPORTANT: Copiez le token IMMÉDIATEMENT
   - Il ne sera affiché qu'une seule fois!

6. **Mettez à jour le .env**
   ```bash
   nano /home/user/bmad-gitea-bridge/.env
   ```

   Remplacez la ligne:
   ```
   GITEA_ADMIN_TOKEN=84e40f124f2a4cc38f2b87435bd4d280f0653da2
   ```

   Par:
   ```
   GITEA_ADMIN_TOKEN=votre_nouveau_token_ici
   ```

7. **Testez la connexion**
   ```bash
   cd /home/user/bmad-gitea-bridge
   python3 test_gitea_connection.py
   ```

## Problèmes possibles:

### Token expiré
- Les tokens peuvent avoir une date d'expiration
- Générez-en un nouveau si le vôtre a expiré

### Permissions insuffisantes
- Le compte doit être administrateur Gitea
- Le token doit avoir les permissions complètes

### Repository inexistant
- Vérifiez que le repository `projet-medical-main` existe dans Gitea
- Si non, créez-le d'abord manuellement

## Vérification du repository:

1. Allez sur: http://192.168.0.76:3000
2. Vérifiez que le repository `projet-medical-main` existe
3. Si non, créez-le:
   - Cliquez sur "+" (créer)
   - "Nouveau dépôt" / "New Repository"
   - Nom: `projet-medical-main`
   - Privé: Oui (recommandé)
   - Initialisez avec README: Oui

## Une fois le token configuré:

```bash
# Test de connexion
python3 test_gitea_connection.py

# Si succès, test à vide (dry-run)
python3 src/sync.py sync-artifacts -p medical --dry-run

# Si dry-run OK, synchronisation réelle
python3 src/sync.py sync-artifacts -p medical
```
