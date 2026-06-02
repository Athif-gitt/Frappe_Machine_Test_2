# Library Management App

A Library Management System built using Frappe Framework.

## Features

- Manage Library Articles
- Manage Members
- Membership Validation
- Issue/Return Transactions
- Borrow Limit Validation
- Automatic Article Status Updates

---

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js
- Redis
- MariaDB
- Frappe Bench

---

## Installation

### Clone Repository

```bash
git clone <your-github-repo>
```

### Go to bench folder

```bash
cd frappe-bench
```

### Get App

```bash
bench get-app <repo-url>
```

### Install App

```bash
bench --site library.local install-app library_management
```

### Run Migrations

```bash
bench --site library.local migrate
```

### Start Server

```bash
bench start
```

---

## Business Logic

Implemented in:

```text
library_management/library_management/doctype/library_transaction/library_transaction.py
```

Includes:

- Membership validation
- Borrow limit validation
- Automatic article availability updates
