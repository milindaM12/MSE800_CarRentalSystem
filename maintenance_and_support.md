# Car Rental System — Maintenance and Support Plan

**Document Version:** 1.0  
**Course:** MSE800 Professional Software Engineering  
**Author:** Yasas Milinda Manamperi 

---

## 1. Introduction

This document outlines the strategies for maintaining the Car Rental System over time. It covers software maintenance practices, versioning conventions, and backward compatibility policies to ensure the system remains reliable, evolvable, and professionally managed.

---

## 2. Managing Software Maintenance

### 2.1 Types of Maintenance

Software maintenance is classified into four categories, each addressed differently in this system:

| Type | Description | Example |
|---|---|---|
| **Corrective** | Fix defects discovered after release | Fix plain-text password storage |
| **Adaptive** | Update the system to work in new environments | Migrate from SQLite to PostgreSQL |
| **Perfective** | Improve performance or add minor enhancements | Add search/filter to car listing |
| **Preventive** | Refactor to improve future maintainability | Replace sequential car IDs with UUIDs |

### 2.2 Maintenance Workflow

All maintenance follows this lifecycle:

1. **Issue Identification** — Bugs or enhancement requests are logged in a tracking system (e.g., GitHub Issues or Jira).
2. **Triage** — Issues are classified by type (corrective/adaptive/perfective/preventive) and prioritised (Critical / High / Medium / Low).
3. **Branch & Fix** — Work is done on a dedicated branch (e.g., `fix/password-hashing`), never directly on `main`.
4. **Testing** — Unit tests and integration tests are run before merging. Manual regression testing covers all menu paths.
5. **Code Review** — At least one peer review is required before merging.
6. **Release** — A new version is tagged and the changelog is updated.

### 2.3 Testing Strategy

To support safe ongoing maintenance, the following testing approach is recommended:

- **Unit Tests** (`pytest`): Test each model class (`Car`, `User`, `Booking`) and each service method independently using an in-memory SQLite database.
- **Integration Tests**: Simulate full user flows (register → login → book → approve) against a temporary test database.
- **Regression Tests**: A checklist of all CLI menu paths verified manually after each release.

### 2.4 Documentation

- All public methods include docstrings (Google/NumPy style).
- A `CHANGELOG.md` file tracks all changes per version.
- The README is updated with each release.

---

## 3. Versioning

The project follows **Semantic Versioning (SemVer)**: `MAJOR.MINOR.PATCH`

| Component | When to increment | Example |
|---|---|---|
| **MAJOR** | Incompatible API or database schema changes | `1.x.x → 2.0.0` |
| **MINOR** | New backward-compatible features | `1.0.x → 1.1.0` |
| **PATCH** | Backward-compatible bug fixes | `1.1.0 → 1.1.1` |

### 3.1 Current Version History

| Version | Date | Changes |
|---|---|---|
| `1.0.0` | Initial | Core CRUD for cars, users, bookings; approve booking |
| `1.1.0` | Current | Added: update car, reject booking, start date field, loyalty points, docstrings |

### 3.2 Git Branching Strategy

```
main          ← production-ready, tagged releases only
develop       ← integration branch; merges from feature branches
feature/*     ← individual features (e.g., feature/loyalty-points)
fix/*         ← bug fixes (e.g., fix/car-id-collision)
release/*     ← release preparation (e.g., release/1.2.0)
hotfix/*      ← urgent production fixes branched from main
```

### 3.3 Tagging and Changelog

Each release is tagged in Git (`git tag v1.1.0`) and accompanied by a `CHANGELOG.md` entry:

```markdown
## [1.1.0] - 2025-XX-XX
### Added
- Update car feature for admin
- Reject booking with automatic availability restore
- Loyalty points system (innovative feature)
- Start date field in bookings
### Fixed
- Missing docstrings across all modules
- Admin menu missing "update car" option
```

---

## 4. Backward Compatibility

### 4.1 Database Schema Changes

The most critical compatibility concern is the SQLite database schema. The following policy applies:

- **Non-breaking additions** (new optional columns with defaults): handled with `ALTER TABLE ... ADD COLUMN`. Existing data is unaffected.
- **Breaking changes** (renaming, removing, changing column types): require a **migration script** and a MAJOR version bump.

#### Migration Example

If the `start_date` column is added to an existing `bookings` table:

```python
def migrate_v1_to_v1_1():
    conn = get_connection()
    cursor = conn.cursor()
    # Add column only if it doesn't exist
    cursor.execute("PRAGMA table_info(bookings)")
    cols = [row[1] for row in cursor.fetchall()]
    if "start_date" not in cols:
        cursor.execute(
            "ALTER TABLE bookings ADD COLUMN start_date TEXT NOT NULL DEFAULT '2025-01-01'"
        )
    conn.commit()
    conn.close()
```

Migration scripts are versioned alongside the code and run automatically at startup when the detected schema version is below the current version.

### 4.2 API / Interface Compatibility

Because this is a CLI application with no external API, backward compatibility primarily concerns:

- **Data format compatibility**: `to_dict()` and `from_dict()` methods on all models must handle both old and new schema fields gracefully (use `.get()` with defaults for new optional fields).
- **Database compatibility**: All migrations are additive and non-destructive wherever possible.

### 4.3 Python Version Compatibility

- Minimum supported version: **Python 3.10** (for `X | None` union syntax).
- The code avoids third-party dependencies, ensuring compatibility across standard Python installations.
- Future versions targeting Python 3.12+ may use `match/case` statements for menu dispatch.

---

## 5. Long-Term Evolution Roadmap

| Phase | Feature | Justification |
|---|---|---|
| **v1.2** | Password hashing (bcrypt) | Security — plain-text passwords are a critical vulnerability |
| **v1.3** | UUID-based car IDs | Prevents ID collision after deletions |
| **v2.0** | REST API (FastAPI) | Enables web/mobile front-ends; marks a MAJOR interface change |
| **v2.1** | PostgreSQL backend | Scalability beyond single-file SQLite |
| **v2.2** | Web dashboard (React) | Replaces CLI for better UX |
| **v3.0** | IoT integration | Real-time car GPS tracking and keyless entry |

---

## 6. Importance of Software Engineering Principles

The long-term success of the Car Rental System depends on adherence to software engineering principles:

- **Separation of Concerns**: The Model–Service–UI architecture means each layer can evolve independently. Swapping SQLite for PostgreSQL only requires changes in `db.py` and the service layer.
- **Encapsulation**: Private attributes and getter methods ensure internal state cannot be corrupted by external code.
- **Open/Closed Principle**: New vehicle types (e.g., `Truck`, `Van`) can be added by subclassing `Vehicle` without modifying existing code.
- **DRY (Don't Repeat Yourself)**: The `get_connection()` factory is the single point of database configuration.
- **Continuous Documentation**: Docstrings, the README, and the changelog ensure the system remains understandable as the team or codebase grows.

These principles reduce the cost of change over time — the defining measure of a well-maintained software system.