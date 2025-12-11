# STITCHLESS™ App Specificatie

## Platform Keuze

- [x] **Web App (Next.js + PWA)** - Aanbevolen voor snelle start
- [ ] iOS Native (Swift)
- [ ] Cross-platform (React Native/Flutter)

---

## MVP Functies

### Pagina's

| Pagina | Beschrijving | Prioriteit |
|--------|--------------|------------|
| Landing Page | Hero, voordelen, doelgroepen | MVP |
| Product Catalogus | Kits voor ouders/sporters/bouwvak | MVP |
| Pre-order Funnel | Email capture, wachtlijst | MVP |
| Checkout | Bestelformulier + betaling | MVP |
| Instructies | Video's en gebruiksaanwijzing | V2 |
| Admin Dashboard | Bestellingen beheren | V2 |

---

## Technische Stack

```
Frontend:     Next.js 14 + React
Styling:      Tailwind CSS
Database:     Supabase (PostgreSQL)
Authenticatie: Supabase Auth
Betalingen:   Stripe / Mollie (iDEAL)
Email:        Resend
Hosting:      Vercel
Analytics:    Vercel Analytics
```

---

## Dropshipping Integratie

### Order Flow

```
[Klant plaatst bestelling]
        ↓
[Betaling via Stripe/Mollie]
        ↓
[Order in database + bevestigingsmail]
        ↓
[Automatische notificatie naar leverancier]
        ↓
[Leverancier verzend met STITCHLESS™ branding]
        ↓
[Tracking update naar klant]
```

### Kwaliteitseisen (99,9% SLA)

- [ ] Steriele productie verificatie
- [ ] Poka-yoke ontwerp check
- [ ] Soft-pull limiet test
- [ ] QC-tests documentatie

---

## Doelgroepen

| Segment | Beschrijving | Specifieke Features |
|---------|--------------|---------------------|
| Ouders | Gezinnen met kinderen | Kindvriendelijke instructies |
| Sporters | Atleten, fitness | Compacte kit, snelle toepassing |
| Bouwvak | Professionals | Robuuste verpakking, bulk opties |

---

## Design Richtlijnen

### Kleuren (aan te passen)

```css
--primary:    #0066CC;    /* Betrouwbaar blauw */
--secondary:  #00AA66;    /* Medisch groen */
--accent:     #FF6600;    /* Call-to-action oranje */
--background: #FFFFFF;    /* Schoon wit */
--text:       #333333;    /* Leesbaar donkergrijs */
```

### Stijl

- Modern en clean
- Medisch/professioneel uitstraling
- Vertrouwenwekkend
- Mobiel-eerst ontwerp

---

## Database Schema (Basis)

```sql
-- Producten
products:
  - id
  - name
  - description
  - price
  - target_audience (ouders/sporters/bouwvak)
  - image_url
  - stock_status

-- Bestellingen
orders:
  - id
  - customer_email
  - customer_name
  - shipping_address
  - product_id
  - quantity
  - total_price
  - status (pending/paid/shipped/delivered)
  - created_at

-- Wachtlijst
waitlist:
  - id
  - email
  - target_audience
  - created_at
```

---

## API Endpoints

```
GET    /api/products          - Alle producten
GET    /api/products/:id      - Product details
POST   /api/orders            - Nieuwe bestelling
GET    /api/orders/:id        - Order status
POST   /api/waitlist          - Aanmelden wachtlijst
POST   /api/webhook/stripe    - Betaling webhook
POST   /api/webhook/supplier  - Leverancier updates
```

---

## Volgende Stappen

1. [ ] Logo en huisstijl aanleveren
2. [ ] Stripe/Mollie account aanmaken
3. [ ] Product foto's en beschrijvingen
4. [ ] Leverancier API/contact details
5. [ ] Domein kiezen (stitchless.nl?)

---

## Prompt voor Development

```
Bouw de STITCHLESS™ webapp volgens bovenstaande specificaties.

Start met:
1. Next.js project setup met Tailwind
2. Landing page met hero en product sectie
3. Pre-order/wachtlijst formulier
4. Supabase database connectie
5. Basis checkout flow

Tech: Next.js 14, Tailwind CSS, Supabase, Stripe
```

---

*Pas dit document aan met je specifieke wensen voordat we beginnen met bouwen.*
