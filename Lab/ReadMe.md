# Testing Lab

---

## Informations

---

```mermaid

flowchart TD
  A("Main Station") --> B("SIEM")
    D("Kali") --> B
    E("Domain Controller") --> B
    F("Windows 10") --> B
    H("Ubuntu") --> B
    I("Windows Server") --> B
    B --> G("SOAR")
    E --> I
    I --> E
    G --> D
    G --> E
    G --> F
    G --> H
    G --> I

```
