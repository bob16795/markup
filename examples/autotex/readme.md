# Replace autotex / autormd with markup

file structure

```
Documents
├── pdf
│   ├── chapter1.pdf
│   ├── chapter2.pdf
│   ├── master.pdf
│   ├── subject1_document1.pdf
│   ├── subject1_document2.pdf
│   ├── subject2_document1.pdf
│   ├── subject2_document2.pdf
│   ├── subject3_document1.pdf
│   └── subject3_document2.pdf
└── src
    ├── chapter1
    │   ├── main.mu                -> main.mu
    │   ├── subject1_master.mu     -> subject.mu
    │   ├── subject1_document1.mu  -> document.mu
    │   └── subject1_document2.mu  -> document.mu
    ├── chapter2
    │   ├── main.mu                -> main.mu
    │   ├── subject2_master.mu     -> subject.mu
    │   ├── subject2_document1.mu  -> document.mu
    │   ├── subject2_document2.mu  -> document.mu
    │   ├── subject3_master.mu     -> subject.mu
    │   ├── subject3_document1.mu  -> document.mu
    │   └── subject3_document2.mu  -> document.mu
    └── master.mu                  -> master.mu
```
