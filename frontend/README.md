# Frontend (Next.js)

Admin UI for the e-commerce microservices. Talks **only** to the API Gateway
(`http://localhost:8000`) — it never calls individual services directly.

## Stack

- Next.js 15 (App Router) + React 19
- TypeScript
- Tailwind CSS (utility classes)
- TanStack Query (server state / caching)
- React Hook Form + Zod (forms + validation)
- Sonner (toast notifications)
- lucide-react (icons)

## Layout

```
frontend/
├── app/
│   ├── globals.css
│   ├── layout.tsx          # root layout + providers + shell
│   ├── page.tsx            # dashboard
│   ├── providers.tsx       # QueryClient + Toaster
│   └── users/
│       └── page.tsx
├── components/
│   ├── layout/
│   │   └── app-shell.tsx
│   ├── ui/                 # primitives (button, card, input, label, table)
│   └── users/
│       ├── create-user-form.tsx
│       └── users-table.tsx
├── hooks/
│   └── use-users.ts
├── lib/
│   ├── api/
│   │   ├── client.ts       # tiny fetch wrapper + ApiError
│   │   └── users.ts
│   ├── schemas/
│   │   └── user.ts         # zod schemas
│   └── utils.ts
├── .env.local.example
├── next.config.mjs
├── package.json
├── postcss.config.mjs
├── tailwind.config.ts
└── tsconfig.json
```

## Run it

From the repo root:

```bash
cp frontend/.env.local.example frontend/.env.local
make frontend-install
make frontend-dev          # http://localhost:3000
```

Or directly:

```bash
cd frontend
npm install
npm run dev
```

Make sure the backend gateway is reachable at `NEXT_PUBLIC_API_BASE_URL`
(default `http://localhost:8000`). Start it with `make compose-up` from the
repo root.

## Implemented so far

- **Dashboard** (`/`) — landing page with section cards
- **Users** (`/users`) — list users + create user form

## Coming next

- `/products` — list + create
- `/orders` — create order with multiple items, list, cancel, detail page
