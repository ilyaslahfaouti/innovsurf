# Rapport Simple des Tests d'API

**Date:** 2025-08-27 02:20:45

## Résumé

- **Total:** 12
- **Succès:** 2 ✅
- **Échecs:** 10 ❌
- **Taux:** 16.7%

## Détails

### ✅ Spots de surf

- **URL:** `http://localhost:8000/api/surf-spots/`
- **Méthode:** GET
- **Statut:** 200
- **Temps:** 0.03s
- **Taille:** 727 caractères

---

### ❌ Détail spot

- **URL:** `http://localhost:8000/api/surf-spots/1/`
- **Méthode:** GET
- **Statut:** 401
- **Temps:** 0.01s
- **Taille:** 59 caractères

---

### ✅ Prévisions

- **URL:** `http://localhost:8000/api/surf-spots/prevision/1/`
- **Méthode:** GET
- **Statut:** 200
- **Temps:** 0.74s
- **Taille:** 10138 caractères

---

### ❌ Clubs de surf

- **URL:** `http://localhost:8000/api/surf-clubs/`
- **Méthode:** GET
- **Statut:** 404
- **Temps:** 0.01s
- **Taille:** 12604 caractères

---

### ❌ Leçons

- **URL:** `http://localhost:8000/api/lessons/`
- **Méthode:** GET
- **Statut:** 404
- **Temps:** 0.01s
- **Taille:** 12595 caractères

---

### ❌ Réservations

- **URL:** `http://localhost:8000/api/bookings/`
- **Méthode:** GET
- **Statut:** 404
- **Temps:** 0.01s
- **Taille:** 12598 caractères

---

### ❌ Utilisateurs

- **URL:** `http://localhost:8000/api/users/`
- **Méthode:** GET
- **Statut:** 404
- **Temps:** 0.01s
- **Taille:** 12589 caractères

---

### ❌ Chatbot

- **URL:** `http://localhost:8000/api/chatbot/`
- **Méthode:** GET
- **Statut:** 400
- **Temps:** 0.00s
- **Taille:** 30 caractères

---

### ❌ Analytics

- **URL:** `http://localhost:8000/api/analytics/dashboard/`
- **Méthode:** GET
- **Statut:** 404
- **Temps:** 0.01s
- **Taille:** 12631 caractères

---

### ❌ Recommandations

- **URL:** `http://localhost:8000/api/recommendations/`
- **Méthode:** GET
- **Statut:** 404
- **Temps:** 0.01s
- **Taille:** 12619 caractères

---

### ❌ Créer leçon

- **URL:** `http://localhost:8000/api/lessons/`
- **Méthode:** POST
- **Statut:** 404
- **Temps:** 0.01s
- **Taille:** 12596 caractères

---

### ❌ Créer réservation

- **URL:** `http://localhost:8000/api/bookings/`
- **Méthode:** POST
- **Statut:** 404
- **Temps:** 0.02s
- **Taille:** 12599 caractères

---

